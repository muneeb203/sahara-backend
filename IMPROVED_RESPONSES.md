# Improved Response System for Sensitive Queries

## 🎯 What Changed

The chatbot now handles sensitive situations (like domestic violence) with a **three-step approach**:

### Step 1: Immediate Safety & Empathy
When a user mentions violence, abuse, or crisis, the chatbot:
- Shows empathy and validates their feelings
- Provides **immediate safety actions** (emergency numbers, safe places)
- Reassures them they're not alone

### Step 2: User Choice
Asks the user to choose:
- **A**: Legal guidance (Pakistani law)
- **B**: Islamic guidance (authentic hadith)
- **C**: Both perspectives

### Step 3: Detailed, Referenced Response
Based on their choice, provides:
- Specific law sections OR hadith references
- Step-by-step guidance
- Practical actions
- Rights and protections

---

## 📝 Example Interaction

### User Query:
> "My husband beats me, what should I do?"

### Chatbot Response (Step 1):
```
I'm so sorry you're going through this. Your safety is the most important thing right now.

**IMMEDIATE ACTIONS:**
1. If you're in immediate danger, call **1122** (Emergency) or **15** (Police)
2. Go to a safe place - friend, family, or neighbor
3. If injured, seek medical help immediately
4. Call Women Helpline: **1099** (24/7 support)

**You are not alone. This is not your fault.**

Would you like to know more about:
A) **Your legal rights and protections** under Pakistani law
B) **Islamic guidance** on this matter
C) **Both** legal and Islamic perspectives

Please type 'A', 'B', or 'C' to continue, or ask another question.
```

### User Types: "A"

### Chatbot Response (Step 2 - Legal):
```
**LEGAL PROTECTIONS UNDER PAKISTANI LAW:**

1. **Protection of Women (Criminal Laws Amendment) Act, 2006**
   - Section 498-A: Criminalizes domestic violence
   - Punishment: Up to 3 years imprisonment and/or fine

2. **Pakistan Penal Code**
   - Section 337: Hurt (physical injury)
   - Section 354: Assault with intent to outrage modesty
   - Section 506: Criminal intimidation

**IMMEDIATE LEGAL ACTIONS:**

Step 1: File an FIR (First Information Report)
- Go to nearest police station
- File complaint under Section 498-A
- Police must register your complaint

Step 2: Obtain Protection Order
- Apply to Magistrate for protection order
- Court can order husband to stay away
- Violation is punishable offense

Step 3: Medical Documentation
- Get medical examination (medico-legal certificate)
- Document all injuries
- Keep copies for legal proceedings

Step 4: Seek Legal Aid
- Contact District Legal Aid Office
- Free legal assistance available
- Lawyer can guide you through process

**YOUR RIGHTS:**
- Right to live without violence
- Right to file criminal complaint
- Right to maintenance even if separated
- Right to custody of children
- Right to residence (cannot be thrown out)

**WHERE TO GO:**
- Police Station: File FIR
- Women's Police Station: Specialized support
- District Court: Protection orders
- Legal Aid Office: Free legal help

**Sources:**
1. Protection of Women (Criminal Laws Amendment) Act, 2006 (Section 498-A)
2. Pakistan Penal Code (Sections 337, 354, 506)
3. Case Study: Domestic Violence Cases in Pakistan

*Note: This is educational information. Please consult a lawyer for your specific situation.*
```

### User Types: "B"

### Chatbot Response (Step 2 - Islamic):
```
**ISLAMIC GUIDANCE ON DOMESTIC VIOLENCE:**

**What Islam Says:**

1. **Violence is Prohibited**
   - The Prophet Muhammad (ﷺ) said: "The best of you are those who are best to their wives" (Tirmidhi 1162)
   - He never raised his hand against any woman (Sahih Muslim 2328)

2. **Your Rights in Islam**
   - Right to kind treatment: "Live with them in kindness" (Quran 4:19)
   - Right to safety and protection
   - Right to dignity and respect
   - Right to seek divorce if harmed

3. **What You Can Do (Islamically Permissible):**

   a) **Seek Help from Family:**
      - Involve elders or mediators
      - Islamic principle of reconciliation (Sulh)
      - Quran 4:35: "If you fear a breach between them, appoint arbiters"

   b) **Seek Divorce (Khula):**
      - You have the right to seek divorce
      - If husband is abusive, Khula is permissible
      - You may need to return mahr (dowry)

   c) **Separate for Safety:**
      - Protecting yourself is obligatory
      - Preservation of life is a higher priority
      - Temporary or permanent separation is allowed

4. **What Islam Does NOT Allow:**
   - Beating that causes injury
   - Humiliation or degradation
   - Psychological abuse
   - Forcing you to stay in danger

**Authentic Hadith References:**

1. "The most perfect of believers in faith are those best in character, and the best of you are the best to their wives" (Tirmidhi 1162)

2. "A believer must not hate a believing woman; if he dislikes one of her characteristics, he will be pleased with another" (Sahih Muslim 1469)

3. The Prophet (ﷺ) said in his Farewell Sermon: "Fear Allah regarding women, for you have taken them as a trust from Allah" (Sahih Muslim 1218)

**Practical Islamic Guidance:**

1. Make dua (prayer) for protection and guidance
2. Seek counsel from knowledgeable Islamic scholars
3. Involve family elders for mediation
4. If abuse continues, separation is permissible
5. Your safety is a religious obligation

**Sources:**
1. Sahih Muslim (Hadith 2328, 1469, 1218)
2. Jami' at-Tirmidhi (Hadith 1162)
3. Quran (4:19, 4:35)

*Note: This is educational information. Please consult an Islamic scholar for your specific situation.*
```

---

## 🔑 Key Improvements

### 1. **Immediate Safety First**
- Emergency numbers prominently displayed
- Clear action steps
- No delay in getting help

### 2. **User Control**
- User chooses what guidance they want
- Respects their preference
- Can ask for both perspectives

### 3. **Specific References**
- Exact law sections cited
- Specific hadith numbers provided
- Verifiable sources

### 4. **Structured Responses**
- Clear headings
- Step-by-step instructions
- Easy to follow

### 5. **Empathetic Tone**
- Validates feelings
- Non-judgmental
- Supportive language

---

## 🎯 How to Test

1. **Restart the chatbot:**
   ```bash
   streamlit run app.py
   ```

2. **Try this query:**
   > "My husband beats me, what should I do?"

3. **You should see:**
   - Immediate safety message
   - Options A, B, C

4. **Type "A", "B", or "C"**

5. **You should get:**
   - Detailed, referenced response
   - Specific to your choice
   - With proper citations

---

## 📋 Other Sensitive Topics Handled

The system also handles:
- **Crisis/Suicide**: Immediate mental health resources
- **Harassment**: Legal and Islamic guidance options
- **Abuse**: Safety-first approach
- **Violence**: Emergency contacts first

---

## 🔄 To Apply Changes

The changes are already in the code. Just restart:

```bash
# Stop the current app (Ctrl+C)
# Then restart:
streamlit run app.py
```

---

**Your chatbot now provides better, more structured, and more helpful responses for sensitive situations!** 🎉
