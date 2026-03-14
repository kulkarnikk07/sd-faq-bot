"""
San Diego FAQ Bot - Claude AI Integration
Handles question answering using Claude AI with RAG
"""

import os
from anthropic import Anthropic
from typing import Optional, Dict, List
import json


class SanDiegoBot:
    """FAQ Bot powered by Claude AI"""
    
    def __init__(self, data_loader, api_key: Optional[str] = None):
        """
        Initialize the bot with data loader and Claude API
        
        Args:
            data_loader: SanDiegoDataLoader instance with loaded data
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
        """
        self.data_loader = data_loader
        
        # Initialize Claude API
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"  # Claude Sonnet 4.6
        
        # Build knowledge base context
        self.knowledge_base = self.data_loader.get_knowledge_base_text()
        
        print(f"✅ Bot initialized with {len(self.knowledge_base)} characters of context")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with context"""
        return f"""You are a helpful assistant for San Diego municipal permits and regulations.

You have access to:
1. San Diego municipal code and permit documentation
2. Real permit data from the Development Services Department
3. Neighborhood and community planning district information
4. Zoning designations

Your role is to:
- Answer questions about San Diego permits clearly and accurately
- Help users understand what permits they need for their projects
- Explain permit processes, timelines, and requirements
- Provide information about specific neighborhoods and districts
- Reference specific sections of the municipal code when relevant

Guidelines:
- Be conversational and friendly
- Cite specific sources when available (e.g., "According to the municipal code...")
- If you don't know something, say so and suggest where to find more information
- For complex projects, recommend consulting with Development Services directly
- Always prioritize accuracy over speculation

KNOWLEDGE BASE:
{self.knowledge_base[:50000]}

... (truncated for context length - full data available)

Remember: This information is for guidance only. Users should verify all requirements with the San Diego Development Services Department."""
    
    def ask(self, question: str, max_tokens: int = 2000) -> str:
        """
        Ask a question and get an answer from Claude
        
        Args:
            question: User's question
            max_tokens: Maximum response length
            
        Returns:
            Claude's response as a string
        """
        try:
            # Check if question might benefit from permit search
            permit_context = self._get_relevant_permit_examples(question)
            
            # Build the full question with context
            full_question = question
            if permit_context:
                full_question = f"{question}\n\nRelevant permit examples:\n{permit_context}"
            
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=self._build_system_prompt(),
                messages=[
                    {"role": "user", "content": full_question}
                ]
            )
            
            # Extract text from response
            return response.content[0].text
            
        except Exception as e:
            return f"Error: {str(e)}\n\nPlease check your API key and try again."
    
    def _get_relevant_permit_examples(self, question: str, limit: int = 5) -> str:
        """Get relevant permit examples based on the question"""
        # Extract keywords for permit search
        keywords = ['fence', 'deck', 'electrical', 'plumbing', 'mechanical', 
                   'remodel', 'addition', 'construction', 'building']
        
        for keyword in keywords:
            if keyword in question.lower():
                permits = self.data_loader.search_permits(keyword, limit=limit)
                
                if permits:
                    context_parts = []
                    for i, permit in enumerate(permits[:3], 1):  # Show top 3
                        permit_info = f"{i}. Type: {permit.get('approval_type', 'N/A')}"
                        if 'project_title' in permit:
                            permit_info += f" - {permit['project_title']}"
                        context_parts.append(permit_info)
                    
                    return "\n".join(context_parts)
        
        return ""
    
    def generate_permit_checklist(self, project_description: str) -> str:
        """
        Generate a permit checklist for a project
        
        Args:
            project_description: Description of the project (e.g., "build a deck")
            
        Returns:
            Formatted checklist of required permits
        """
        prompt = f"""Based on this project description, provide a detailed permit checklist:

Project: {project_description}

Please provide:
1. Required permits (be specific)
2. Estimated timeline for approval
3. Approximate costs (if known from the data)
4. Important considerations or requirements
5. Suggested next steps

Format the response as a clear, actionable checklist."""
        
        return self.ask(prompt, max_tokens=3000)
    
    def summarize_for_neighborhood(self, content: str, neighborhood: str) -> str:
        """
        Summarize content (e.g., council meeting) for a specific neighborhood
        
        Args:
            content: Content to summarize (e.g., meeting transcript)
            neighborhood: Neighborhood name
            
        Returns:
            Summarized content relevant to the neighborhood
        """
        # Get neighborhood info
        neighborhood_info = self.data_loader.get_community_info(neighborhood)
        
        context = f"Neighborhood: {neighborhood}"
        if neighborhood_info:
            context += f"\nDistrict info: {json.dumps(neighborhood_info, indent=2)}"
        
        prompt = f"""{context}

Please analyze the following content and extract information relevant to {neighborhood}:

{content}

Provide:
1. Key decisions affecting this neighborhood
2. Upcoming projects or changes
3. Action items for residents
4. Important dates or deadlines

Format as a clear summary for residents of {neighborhood}."""
        
        return self.ask(prompt, max_tokens=3000)
    
    def chat(self, conversation_history: List[Dict[str, str]], new_message: str) -> str:
        """
        Continue a conversation with context
        
        Args:
            conversation_history: List of {"role": "user/assistant", "content": "..."}
            new_message: New user message
            
        Returns:
            Claude's response
        """
        # Add new message to history
        messages = conversation_history + [{"role": "user", "content": new_message}]
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=self._build_system_prompt(),
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error: {str(e)}"


def create_bot(data_loader, api_key: Optional[str] = None) -> SanDiegoBot:
    """
    Factory function to create bot instance
    Compatible with existing app.py
    """
    return SanDiegoBot(data_loader, api_key)


if __name__ == "__main__":
    # Test the bot
    from data_loader import load_data
    
    print("=" * 60)
    print("San Diego Bot Test")
    print("=" * 60)
    
    # Load data
    print("\nLoading data...")
    loader = load_data()
    
    # Create bot
    print("\nInitializing bot...")
    bot = create_bot(loader)
    
    # Test questions
    test_questions = [
        "What permits do I need to build a fence?",
        "How much does a building permit cost?",
        "What is the process for getting a permit approved?"
    ]
    
    print("\n" + "=" * 60)
    print("Testing Questions:")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\nQ: {question}")
        print(f"A: {bot.ask(question)}")
        print("-" * 60)
    
    print("\n✅ Bot test complete!")