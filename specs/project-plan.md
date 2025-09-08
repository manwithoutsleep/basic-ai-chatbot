# AI Chatbot Project Plan
*Spiritual Gifts & Personal Style Discovery Chatbot*

## Project Overview

**Vision:** Build a chatbot that guides users through self-discovery, helping them identify their spiritual gifts and personal style by finding the right balance between skills and passions.

**Primary Goal:** Learning fundamental AI chatbot architecture and orchestration
**Secondary Goal:** Working prototype for friends/family feedback

## 1. Conceptual Architecture & Technology Stack

### High-Level Architecture
```
User Interface (Web/CLI)
    ↓
Conversation Manager (handles state & flow)
    ↓
Core Logic Engine (self-discovery orchestration)
    ↓
LLM API Client (OpenAI/Anthropic/etc.)
    ↓
Knowledge Base (spiritual gifts data, optional vector DB)
```

### Technology Decisions

**Model Choice:** Google Gemini API (selected for initial development)
- **Pros:** Free tier for learning, familiar interface, good performance, generous rate limits
- **Cons:** Newer API with smaller community, potential migration needed later
- **Rationale:** Cost-free learning environment, can migrate to other APIs later
- **Alternative options:** OpenAI GPT-4, Anthropic Claude (for future phases)

**Technology Stack:**
- **Language:** Python (best ecosystem for AI/ML experimentation)
- **Core Libraries:** Start with `requests` and `json` - build own logic first
- **Later additions:** Consider `openai`/`anthropic` SDK, `streamlit` for quick UI
- **Avoid initially:** LangChain/LlamaIndex (add complexity; learn fundamentals first)

**Vector Database:** Start without one
- Begin with simple JSON files for spiritual gifts data
- Use basic keyword matching or structured prompts
- Add vector search later if semantic similarity needed

## 2. Phased Development Roadmap

### Phase 1: Basic API Integration (Week 1) ✓ COMPLETED
- Set up Python environment ✓
- Create simple script that calls LLM API ✓
- Handle API responses and basic error cases ✓
- **Milestone:** "Hello, I'm your spiritual discovery guide" bot ✓

### Phase 2: Conversation Management (Week 2) ✓ COMPLETED
- Implement conversation history storage ✓
- Add session state management ✓
- Create basic conversation flow control ✓
- **Milestone:** Multi-turn conversations with memory ✓

### Phase 3: Self-Discovery Logic Engine (Week 3-4)
- Design question progression system
- Implement skills vs. passions analysis
- Create simple scoring/assessment logic
- Add basic spiritual gifts framework
- **Milestone:** Complete guided discovery session

### Phase 4: Enhanced Intelligence (Week 5)
- Add context-aware responses
- Implement dynamic questioning based on previous answers
- Create personality/style profiling
- **Milestone:** Personalized recommendations

### Phase 5: User Interface (Week 6)
- Build simple web interface (Streamlit or Flask)
- Add conversation export/summary features
- Create results visualization
- **Milestone:** Shareable prototype

## 3. Core Self-Discovery Engine Design

### Recommended Approach: Structured Prompt Chaining
Start with **decision tree + dynamic prompting** approach:

```python
class DiscoverySession:
    stages = ["introduction", "skills_assessment", "passion_exploration", 
              "values_clarification", "synthesis", "recommendations"]
    
    def get_next_question(self, stage, previous_answers):
        # Use structured prompts with context injection
        prompt = self.build_contextual_prompt(stage, previous_answers)
        return llm_api_call(prompt)
```

### Journey Modeling
- **User State:** Track current stage, answered questions, emerging themes
- **Progress Tracking:** Simple JSON state file per session
- **Adaptive Flow:** Branch questions based on previous responses

### Why Not RAG Initially
- Simpler to debug and understand
- Leverages existing programming experience with algorithmic approaches
- Can add RAG later for more sophisticated knowledge retrieval

## 4. Learning Path & Resources

### Phase 1 Learning
- **Concepts:** API integration, JSON handling, prompt engineering
- **Resources:** 
  - Google Gemini API documentation
  - "Prompt Engineering Guide" (promptingguide.ai)

### Phase 2 Learning
- **Concepts:** State management, session persistence
- **Resources:** Existing software engineering knowledge applies directly

### Phase 3 Learning
- **Concepts:** Conversation design, psychological assessment frameworks
- **Resources:**
  - "Conversational Design" by Erika Hall
  - Research spiritual gifts assessments (StrengthsFinder, etc.)

### Phase 4 Learning
- **Concepts:** Context injection, dynamic prompting
- **Resources:** 
  - "Building LLM Applications" articles on towards data science
  - Anthropic's prompt engineering documentation

### Phase 5 Learning
- **Concepts:** Web interfaces, data visualization
- **Resources:** Streamlit documentation, basic HTML/CSS if needed

## 5. First Technical Steps (Today)

### Immediate Actions
1. **Get a Google Gemini API key** ✓ COMPLETED
   - Sign up at Google AI Studio (aistudio.google.com)
   - Generate API key (free tier available)
   - Store securely in .env file
   
2. **Set up development environment:**
   ```bash
   mkdir spiritual-discovery-bot
   cd spiritual-discovery-bot
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install requests python-dotenv
   ```

3. **Create first "hello world" bot:**
   - Make simple script that calls the API
   - Test basic conversation functionality
   - Store API key in `.env` file

### Why This First
Gets you immediately hands-on with core technology while being achievable in 1-2 hours. Learn prompt engineering basics and see how LLM APIs work - fundamental to everything else.

## Next Steps & Iteration

This plan balances learning goals with practical progress. The phased approach ensures understanding of each component before adding complexity, while technology choices leverage existing programming skills.

**Plan Status:** Initial version - to be reviewed and iterated upon
**Next Review:** After completing Phase 1 setup