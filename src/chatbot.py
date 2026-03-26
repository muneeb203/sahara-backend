"""Main RAG chatbot implementation."""

import logging
from typing import List, Dict, Tuple
from datetime import datetime

from retriever import Retriever
from llm_interface import LLaMAInterface
from utils import load_config, setup_logging


logger = logging.getLogger(__name__)


class HerHaqChatbot:
    """RAG-based chatbot for women's rights assistance."""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Initialize components
        logger.info("Initializing HerHaq Chatbot...")
        self.retriever = Retriever(config)
        self.llm = LLaMAInterface(config)
        
        # Load prompts
        self.system_prompt = config['prompts']['system_prompt']
        
        # Conversation history
        self.conversation_history = []
        self.max_history = config['chatbot']['max_history']
        
        logger.info("Chatbot initialized successfully!")
    
    def _add_to_history(self, user_message: str, bot_response: str, sources: List[Dict], is_safety_response: bool = False):
        """Add interaction to conversation history."""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'bot': bot_response,
            'sources': sources,
            'is_safety_response': is_safety_response
        })
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def _safety_check(self, query: str) -> Tuple[bool, str]:
        """Check if query is appropriate and safe."""
        query_lower = query.lower()
        
        # Crisis keywords
        crisis_keywords = ['suicide', 'kill myself', 'harm myself', 'end my life', 'want to die']
        for keyword in crisis_keywords:
            if keyword in query_lower:
                return False, (
                    "I'm deeply concerned about what you're going through. "
                    "Please reach out to a mental health professional or crisis helpline immediately:\n\n"
                    "- Pakistan Mental Health Helpline: 0800-00-00-00\n"
                    "- Rozan (Psychological Support): 0800-22222\n"
                    "- Emergency: 1122\n\n"
                    "Your life matters, and there are people who want to help you."
                )
        
        # Sexual violence keywords - needs special handling
        sexual_violence_keywords = ['rape', 'rapes', 'sexual assault', 'sexual abuse', 'forced sex', 'forces me', 'sexual violence']
        for keyword in sexual_violence_keywords:
            if keyword in query_lower:
                return False, (
                    "I'm deeply sorry you're experiencing this. What you're describing is a serious crime and you deserve safety and support.\n\n"
                    "**IMMEDIATE ACTIONS:**\n"
                    "1. If you're in immediate danger, call **1122** (Emergency) or **15** (Police)\n"
                    "2. Go to a safe place immediately - friend, family, or women's shelter\n"
                    "3. Seek medical help urgently - hospital can provide care and documentation\n"
                    "4. Call War Against Rape Helpline: **0800-22444** (24/7 support)\n"
                    "5. Women Helpline: **1099** | Rozan: **0800-22222**\n\n"
                    "**You are not alone. This is NOT your fault. You deserve safety and respect.**\n\n"
                    "Would you like to know more about:\n"
                    "A) **Your legal rights and protections** under Pakistani law\n"
                    "B) **Islamic guidance** on consent and your rights\n"
                    "C) **Both** legal and Islamic perspectives\n\n"
                    "Please type 'A', 'B', or 'C' to continue, or ask another question."
                )
        
        # Domestic violence keywords - needs special handling
        violence_keywords = ['beats me', 'hitting me', 'abusing me', 'hurts me', 'violent', 'domestic violence', 'physical abuse']
        for keyword in violence_keywords:
            if keyword in query_lower:
                return False, (
                    "I'm so sorry you're going through this. Your safety is the most important thing right now.\n\n"
                    "**IMMEDIATE ACTIONS:**\n"
                    "1. If you're in immediate danger, call **1122** (Emergency) or **15** (Police)\n"
                    "2. Go to a safe place - friend, family, or neighbor\n"
                    "3. If injured, seek medical help immediately\n"
                    "4. Call Women Helpline: **1099** (24/7 support)\n\n"
                    "**You are not alone. This is not your fault.**\n\n"
                    "Would you like to know more about:\n"
                    "A) **Your legal rights and protections** under Pakistani law\n"
                    "B) **Islamic guidance** on this matter\n"
                    "C) **Both** legal and Islamic perspectives\n\n"
                    "Please type 'A', 'B', or 'C' to continue, or ask another question."
                )
        
        return True, ""
    
    def _format_response_with_sources(self, response: str, sources: List[Dict]) -> str:
        """Format response with source citations."""
        # Just add the disclaimer, no sources list at bottom
        formatted_response = response + "\n\n"
        formatted_response += "*Note: This information is for educational purposes. For legal matters, please consult a qualified lawyer.*"
        
        return formatted_response
    
    def _get_preformatted_response(self, choice: str, query_type: str, sources: List[Dict]) -> str:
        """Get pre-formatted response for sensitive topics to avoid LLM safety filters."""
        
        if query_type == 'sexual_violence' and choice == 'A':
            # Legal response for marital rape/sexual violence
            response = """**LEGAL PROTECTIONS AGAINST SEXUAL VIOLENCE:**

**1. CRIMINAL LAWS IN PAKISTAN:**

• **Pakistan Penal Code (PPC)**
  - Section 375: Rape (includes forced sexual intercourse)
  - Section 376: Punishment for rape (10-25 years or life imprisonment)
  - Section 354: Assault with intent to outrage modesty
  - Section 509: Insulting modesty of a woman

• **Criminal Law (Amendment) Act, 2016**
  - Enhanced penalties for sexual offenses
  - Protection for victims during trial
  - Prohibition of character assassination

**2. MARITAL RAPE - YOUR RIGHTS:**

While Pakistani law has limitations regarding marital rape, you have these protections:

✓ Right to refuse sexual relations
✓ Right to bodily autonomy and dignity
✓ Right to file for divorce (Khula) on grounds of cruelty
✓ Right to file complaint for physical harm under PPC Section 337
✓ Right to protection order under domestic violence laws
✓ Right to separate residence

**3. LEGAL ACTIONS YOU CAN TAKE:**

**Immediate Actions:**
- Document all incidents (dates, times, injuries)
- Seek medical examination and get Medico-Legal Certificate
- Take photographs of any injuries
- Keep records of threats or coercion

**Legal Procedures:**

**Step 1: Medical Documentation**
- Visit hospital emergency department
- Request full medical examination
- Get Medico-Legal Certificate (MLC)
- Request forensic evidence collection if recent
- Keep all medical records

**Step 2: File Complaint**
- File FIR at police station for physical harm (Section 337)
- File complaint for assault (Section 354)
- Request female police officer if available
- Get FIR copy for records

**Step 3: Seek Protection**
- Apply for protection order from magistrate
- Request separate residence order
- File for divorce (Khula) citing cruelty
- Seek custody of children if applicable

**Step 4: Legal Representation**
- Contact District Legal Aid Office (free)
- Women's rights organizations provide legal support
- Bar Council legal aid services
- NGOs specializing in women's rights

**4. YOUR LEGAL RIGHTS:**

✓ Right to physical safety and dignity
✓ Right to refuse unwanted sexual contact
✓ Right to divorce on grounds of cruelty
✓ Right to maintenance even after separation
✓ Right to custody of children
✓ Right to residence (cannot be evicted)
✓ Right to privacy during legal proceedings
✓ Right to free legal aid

**5. WHERE TO SEEK HELP:**

• **Police Stations**: File FIR for physical harm
• **Women's Police Stations**: Specialized support
• **District Courts**: Protection orders, divorce
• **Legal Aid Offices**: Free legal representation
• **Women's Crisis Centers**: Counseling and support
• **NGOs**: War Against Rape, Aurat Foundation, Shirkat Gah

**6. SUPPORT ORGANIZATIONS:**

• War Against Rape Helpline: 0800-22444
• Madadgar National Helpline: 1098
• Women Helpline: 1099
• Rozan (Psychological Support): 0800-22222
• Police Emergency: 15
• Emergency Services: 1122

**7. IMPORTANT LEGAL POINTS:**

• Consent is required for all sexual activity
• Force or coercion is illegal even in marriage
• You have the right to say no
• Physical harm is punishable under law
• You can seek divorce for sexual cruelty
• Your testimony is valid and important

**8. SAFETY PLANNING:**

- Keep important documents in safe place
- Have emergency contact numbers ready
- Identify safe places you can go
- Tell trusted person about situation
- Keep some money accessible
- Plan exit strategy if needed

**REMEMBER:**
- This is NOT your fault
- You deserve safety and respect
- Help is available
- You have legal rights
- You are not alone"""
            
            return response
            
        elif query_type == 'sexual_violence' and choice == 'B':
            # Islamic response for sexual violence
            response = """**ISLAMIC TEACHINGS ON SEXUAL RIGHTS AND CONSENT:**

**1. ISLAM'S POSITION ON CONSENT:**

Islam requires mutual consent and kindness in marital relations. Force and coercion are prohibited.

**2. YOUR RIGHTS IN ISLAM:**

✓ Right to refuse sexual relations if:
  - You are ill or in pain
  - You are menstruating
  - You are fasting (during day in Ramadan)
  - You are not willing
  - It causes you harm

✓ Right to kind and gentle treatment
✓ Right to dignity and respect
✓ Right to bodily autonomy
✓ Right to refuse harmful acts
✓ Right to seek divorce for cruelty

**3. QURANIC GUIDANCE:**

• **On Marital Relations:**
  "They are a garment for you and you are a garment for them" (Quran 2:187)
  - This verse emphasizes mutual protection, comfort, and respect

• **On Kind Treatment:**
  "Live with them in kindness" (Quran 4:19)
  - Kindness is mandatory, not optional

• **On Mutual Rights:**
  "Women have rights similar to those of men over them in kindness" (Quran 2:228)

**4. AUTHENTIC HADITH:**

• **Prophet's Teaching on Intimacy:**
  "When a man calls his wife to his bed and she refuses, and he spends the night angry with her, the angels curse her until morning" - This hadith is often misunderstood. Islamic scholars clarify:
  - This applies to unreasonable refusal without valid cause
  - Does NOT permit force or coercion
  - Does NOT override her right to refuse if ill, tired, or unwilling
  - Does NOT permit harmful acts

• **Prophet's Example:**
  "The Prophet (ﷺ) was the most gentle with his wives"
  (Multiple authentic sources)

• **On Treating Wives:**
  "The best of you are those who are best to their wives, and I am the best of you to my wives"
  (Tirmidhi 3895)

**5. ISLAMIC SCHOLARS' CONSENSUS:**

Islamic scholars agree that:
- Force in marital relations is prohibited (Haram)
- Wife's consent and comfort are required
- Causing harm is forbidden
- Dignity must be preserved
- Cruelty is grounds for divorce

**6. WHAT ISLAM PERMITS YOU TO DO:**

**a) Refuse Harmful Acts:**
- You can and should refuse anything harmful
- Protecting your health is obligatory
- Your wellbeing is a religious duty

**b) Seek Divorce (Khula):**
- Sexual cruelty is valid grounds for Khula
- You have the right to end harmful marriage
- Islamic courts recognize this as legitimate reason
- May need to return mahr (dowry)

**c) Seek Family/Community Help:**
- Involve trusted family elders
- Consult knowledgeable Islamic scholars
- Seek help from mosque imam
- Contact Muslim women's organizations

**d) Separate for Safety:**
- Temporary separation is permissible
- Protecting yourself is obligatory (Fard)
- Your safety is a higher Islamic priority
- Permanent separation through divorce is allowed

**7. WHAT ISLAM PROHIBITS:**

✗ Force or coercion in intimate relations
✗ Causing physical or emotional harm
✗ Ignoring spouse's pain or discomfort
✗ Degrading or humiliating treatment
✗ Any act that causes injury
✗ Forcing someone to stay in harmful situation

**8. SCHOLARLY OPINIONS:**

**Sheikh Yusuf al-Qaradawi:**
"The husband has no right to force his wife if she has a legitimate excuse or if it would harm her."

**Islamic Fiqh Council:**
"Marital relations must be based on mutual consent, kindness, and consideration for the wife's physical and emotional state."

**9. YOUR ISLAMIC RIGHTS:**

✓ Right to kind treatment (Quran 4:19)
✓ Right to refuse if valid reason
✓ Right to seek divorce for cruelty
✓ Right to involve family for mediation
✓ Right to protection from harm
✓ Right to dignity and respect
✓ Right to consult Islamic scholars

**10. PRACTICAL ISLAMIC GUIDANCE:**

**Immediate Steps:**
- Make dua (prayer) for protection and guidance
- Seek help from trusted Muslim family/friends
- Consult knowledgeable Islamic scholar
- Contact Muslim women's support organizations
- Remember: protecting your life and health is Fard (obligatory)

**Long-term Options:**
- Family mediation (Islamic principle of Sulh)
- Counseling with Islamic perspective
- Separation if harm continues
- Divorce (Khula) if necessary
- Community support and protection

**IMPORTANT ISLAMIC PRINCIPLES:**

1. **Preservation of Life**: Protecting your physical and mental health is a religious obligation
2. **No Harm Principle**: "There should be neither harming nor reciprocating harm" (Hadith)
3. **Dignity**: Every human has inherent dignity from Allah
4. **Justice**: Islam requires justice even in marriage
5. **Mercy**: Marriage should be based on mercy and compassion

**REMEMBER:**
- Islam values your dignity and wellbeing
- You have rights that must be respected
- Seeking help is not against Islam
- Protecting yourself is a religious duty
- Allah is with those who are oppressed"""
            
            return response
            
        elif query_type == 'sexual_violence' and choice == 'C':
            # Both perspectives
            return self._get_preformatted_response('A', query_type, sources) + "\n\n" + "="*80 + "\n\n" + self._get_preformatted_response('B', query_type, sources)
        
        elif query_type == 'domestic_violence' and choice == 'A':
            # Legal response for domestic violence
            response = """**LEGAL PROTECTIONS UNDER PAKISTANI LAW:**

**1. Criminal Laws:**

• **Protection of Women (Criminal Laws Amendment) Act, 2006**
  - Section 498-A: Criminalizes domestic violence
  - Punishment: Imprisonment up to 3 years and/or fine up to Rs. 500,000

• **Pakistan Penal Code (PPC)**
  - Section 337: Hurt (causing physical injury)
  - Section 354: Assault with intent to outrage modesty
  - Section 506: Criminal intimidation
  - Section 509: Insulting modesty of a woman

**2. YOUR LEGAL RIGHTS:**

✓ Right to file FIR (First Information Report) at any police station
✓ Right to protection order from magistrate
✓ Right to residence (cannot be evicted from home)
✓ Right to maintenance even if separated
✓ Right to custody of children
✓ Right to medical examination and documentation

**3. LEGAL PROCEDURES AVAILABLE:**

**Step 1: File FIR**
- Go to nearest police station
- File complaint under Section 498-A
- Police must register your complaint (mandatory)
- Get FIR copy for your records

**Step 2: Medical Documentation**
- Visit hospital for medical examination
- Request Medico-Legal Certificate (MLC)
- Document all injuries with photographs
- Keep all medical records

**Step 3: Protection Order**
- Apply to local Magistrate
- Court can order abuser to stay away
- Violation of order is punishable offense
- Usually granted within 7 days

**Step 4: Legal Aid**
- Contact District Legal Aid Office (free)
- Women's Police Station (specialized support)
- Legal Aid Society of Pakistan
- Bar Council legal aid services

**4. WHERE TO FILE COMPLAINTS:**

• Police Station: FIR under PPC sections
• Women's Police Station: Specialized handling
• Magistrate Court: Protection orders
• District Court: Divorce/separation cases
• Human Rights Commission: Rights violations

**5. ADDITIONAL PROTECTIONS:**

• Domestic Violence (Prevention and Protection) Act (in some provinces)
• Right to shelter in Dar-ul-Aman (women's shelter)
• Right to free legal representation
• Right to privacy during proceedings
• Protection from retaliation

**IMPORTANT CONTACTS:**
• Women Helpline: 1099
• Police Emergency: 15
• Emergency Services: 1122
• Legal Aid: Contact local Bar Council"""
            
            return response
            
        elif query_type == 'domestic_violence' and choice == 'B':
            # Islamic response for domestic violence
            response = """**ISLAMIC TEACHINGS ON DOMESTIC VIOLENCE:**

**1. ISLAM'S POSITION:**

Islam strictly prohibits violence and abuse in marriage. The Prophet Muhammad (ﷺ) never raised his hand against any woman and condemned such behavior.

**2. AUTHENTIC HADITH:**

• **Prophet's Teaching:**
  "The best of you are those who are best to their wives" 
  (Jami' at-Tirmidhi 1162)

• **Prophet's Example:**
  "The Prophet (ﷺ) never struck a servant or a woman"
  (Sahih Muslim 2328)

• **Farewell Sermon:**
  "Fear Allah regarding women, for you have taken them as a trust from Allah"
  (Sahih Muslim 1218)

• **On Good Treatment:**
  "A believer must not hate a believing woman; if he dislikes one of her characteristics, he will be pleased with another"
  (Sahih Muslim 1469)

**3. YOUR RIGHTS IN ISLAM:**

✓ Right to kind and respectful treatment
✓ Right to safety and protection
✓ Right to dignity and honor
✓ Right to seek divorce (Khula) if harmed
✓ Right to involve family/community for help
✓ Right to separate for your safety

**4. WHAT ISLAM PERMITS YOU TO DO:**

**a) Seek Family Mediation:**
- Involve trusted family elders
- Islamic principle of reconciliation (Sulh)
- Quran 4:35: "Appoint arbiters from both families"

**b) Seek Divorce (Khula):**
- You have the right to seek divorce
- If husband is abusive, Khula is permissible
- May need to return mahr (dowry)
- Your safety takes priority

**c) Separate for Safety:**
- Protecting your life is obligatory (Fard)
- Preservation of life is a higher Islamic priority
- Temporary or permanent separation is allowed
- You are not obligated to stay in danger

**d) Seek Community Help:**
- Consult Islamic scholars
- Involve mosque imam or community leaders
- Seek help from Muslim women's organizations

**5. WHAT ISLAM PROHIBITS:**

✗ Physical violence causing harm
✗ Psychological abuse and humiliation
✗ Degrading treatment
✗ Forcing someone to stay in danger
✗ Denying basic rights

**6. QURANIC GUIDANCE:**

• "Live with them in kindness" (Quran 4:19)
• "They (wives) have rights similar to those (of husbands) over them in kindness" (Quran 2:228)

**7. ISLAMIC SCHOLARS' CONSENSUS:**

Islamic scholars agree that:
- Abuse is not permitted in Islam
- A woman can seek divorce for abuse
- Protecting one's life is a religious duty
- Community should support victims

**SPIRITUAL GUIDANCE:**
• Make dua (prayer) for protection and guidance
• Seek Allah's help in your situation
• Your safety is a religious obligation
• Islam values your dignity and wellbeing"""
            
            return response
            
        elif query_type == 'domestic_violence' and choice == 'C':
            # Both perspectives
            return self._get_preformatted_response('A', query_type, sources) + "\n\n" + "="*80 + "\n\n" + self._get_preformatted_response('B', query_type, sources)
        
        return None
    
    def _handle_followup_choice(self, choice: str, original_query: str) -> Dict:
        """Handle user's choice for legal/Islamic guidance."""
        choice = choice.strip().upper()
        
        # Detect if this is a sensitive topic
        query_lower = original_query.lower()
        query_type = None
        
        # Check for sexual violence first (more specific)
        if any(keyword in query_lower for keyword in ['rape', 'rapes', 'sexual assault', 'sexual abuse', 'forced sex', 'forces me', 'sexual violence']):
            query_type = 'sexual_violence'
        # Then check for general domestic violence
        elif any(keyword in query_lower for keyword in ['beats', 'hitting', 'abusing', 'hurts', 'violent', 'domestic violence', 'physical abuse']):
            query_type = 'domestic_violence'
        
        # Get sources
        modified_query = original_query
        context, sources = self.retriever.retrieve_with_context(modified_query)
        
        # Try to get pre-formatted response for sensitive topics
        if query_type:
            preformatted = self._get_preformatted_response(choice, query_type, sources)
            if preformatted:
                return {
                    'response': self._format_response_with_sources(preformatted, sources),
                    'sources': sources,
                    'context': context,
                    'is_safety_response': False
                }
        
        # For non-sensitive topics or if no pre-formatted response, use LLM
        if choice == 'A':
            # Legal guidance
            legal_sources = [s for s in sources if s['metadata']['source_type'] == 'law']
            if legal_sources:
                sources = legal_sources[:5]
            
            prompt = f"""You are an educational assistant explaining Pakistani law. A person asks: {original_query}

Based on the following legal information from Pakistani law:
{context}

Provide an educational explanation covering:
1. What Pakistani laws say about this situation (cite specific sections)
2. What legal protections exist under Pakistani law
3. What legal procedures are available in Pakistan
4. What rights are guaranteed under Pakistani law
5. Where legal complaints can be filed in Pakistan

This is for educational purposes to help someone understand their legal rights in Pakistan. Always cite specific law sections."""
            
        elif choice == 'B':
            # Islamic guidance
            islamic_sources = [s for s in sources if s['metadata']['source_type'] == 'hadith']
            if islamic_sources:
                sources = islamic_sources[:5]
            
            prompt = f"""You are an educational assistant explaining Islamic teachings. A person asks: {original_query}

Based on the following authentic Islamic sources:
{context}

Provide an educational explanation covering:
1. What Islamic teachings say about this situation (cite specific hadith)
2. What rights exist according to Islamic law
3. What authentic hadith teach about this
4. What Islamic scholars have said about similar situations
5. What options are available according to Islamic jurisprudence

This is for educational purposes to help someone understand Islamic teachings. Always cite specific hadith references with source names."""
            
        elif choice == 'C':
            # Both perspectives
            prompt = f"""You are an educational assistant. A person asks: {original_query}

Based on the following information from Pakistani law and Islamic sources:
{context}

Provide an educational explanation with two sections:

**LEGAL PERSPECTIVE (Pakistani Law):**
Explain what Pakistani laws say about this situation, what legal protections exist, and what legal procedures are available. Cite specific law sections.

**ISLAMIC PERSPECTIVE:**
Explain what Islamic teachings say about this situation based on authentic hadith and Islamic jurisprudence. Cite specific hadith references.

This is for educational purposes to help someone understand both legal and religious perspectives."""
            
        else:
            return {
                'response': "Please choose A, B, or C to continue, or ask a new question.",
                'sources': [],
                'context': '',
                'is_safety_response': True
            }
        
        # Generate response
        raw_response = self.llm.generate(prompt)
        formatted_response = self._format_response_with_sources(raw_response, sources)
        
        return {
            'response': formatted_response,
            'sources': sources,
            'context': context,
            'is_safety_response': False
        }
    
    def chat(self, user_message: str) -> Dict:
        """Process user message and generate response."""
        logger.info(f"User query: {user_message}")
        
        # Check if this is a follow-up choice (A, B, or C)
        if user_message.strip().upper() in ['A', 'B', 'C'] and len(self.conversation_history) > 0:
            last_interaction = self.conversation_history[-1]
            if last_interaction.get('is_safety_response') and 'Would you like to know more about' in last_interaction.get('bot', ''):
                # This is a follow-up to a safety response
                # Extract the original query from history
                if len(self.conversation_history) > 0:
                    original_query = last_interaction.get('user', '')
                    return self._handle_followup_choice(user_message, original_query)
        
        # Safety check
        is_safe, safety_message = self._safety_check(user_message)
        if not is_safe:
            result = {
                'response': safety_message,
                'sources': [],
                'context': '',
                'is_safety_response': True
            }
            # Add to history with safety flag
            self._add_to_history(user_message, safety_message, [], is_safety_response=True)
            return result
        
        # Retrieve relevant context
        logger.info("Retrieving relevant context...")
        context, sources = self.retriever.retrieve_with_context(user_message)
        
        # Generate response
        logger.info("Generating response...")
        prompt = self.llm.format_prompt(self.system_prompt, user_message, context)
        raw_response = self.llm.generate(prompt)
        
        # Format response with sources
        formatted_response = self._format_response_with_sources(raw_response, sources)
        
        # Add to history
        self._add_to_history(user_message, formatted_response, sources)
        
        return {
            'response': formatted_response,
            'sources': sources,
            'context': context,
            'is_safety_response': False
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")


def main():
    """Run chatbot in CLI mode."""
    # Setup logging
    setup_logging()
    
    # Load config
    config = load_config()
    
    # Initialize chatbot
    chatbot = HerHaqChatbot(config)
    
    print("\n" + "="*80)
    print("HerHaq Chatbot - Women's Rights Assistant")
    print("="*80)
    print("\nWelcome! I'm here to help you understand your rights under Pakistani law")
    print("and Islamic guidance. Ask me anything about:")
    print("  - Inheritance rights")
    print("  - Marriage and divorce")
    print("  - Workplace harassment")
    print("  - Property rights")
    print("  - Legal protections")
    print("\nType 'quit' or 'exit' to end the conversation.")
    print("Type 'clear' to clear conversation history.")
    print("="*80 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nThank you for using HerHaq Chatbot. Take care!")
                break
            
            # Check for clear command
            if user_input.lower() == 'clear':
                chatbot.clear_history()
                print("\nConversation history cleared.\n")
                continue
            
            # Get response
            result = chatbot.chat(user_input)
            
            # Display response
            print(f"\nHerHaq: {result['response']}\n")
            
            # Display sources if not safety response
            if not result['is_safety_response'] and result['sources']:
                print("Retrieved sources:")
                for idx, source in enumerate(result['sources'], 1):
                    print(f"  {idx}. {source['citation']} (Relevance: {source['score']:.2f})")
                print()
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\nI apologize, but I encountered an error. Please try again.\n")


if __name__ == "__main__":
    main()
