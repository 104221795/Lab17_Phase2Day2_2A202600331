BENCHMARK_CONVERSATIONS = [
    {
        "id": "case_01_profile_allergy_conflict",
        "scenario": "Allergy conflict update",
        "turns": [
            "Tôi dị ứng sữa bò.",
            "À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò.",
            "Tôi dị ứng gì?"
        ],
        "expected_keywords": ["đậu nành"],
        "category": "profile recall + conflict update"
    },
    {
        "id": "case_02_profile_response_preference",
        "scenario": "Recall response style preference",
        "turns": [
            "Tôi thích câu trả lời ngắn.",
            "Sau 5 lượt nữa bạn vẫn cần nhớ preference này.",
            "Bạn nên trả lời theo style nào?"
        ],
        "expected_keywords": ["brief"],
        "category": "profile recall"
    },
    {
        "id": "case_03_profile_name_recall_after_noise",
        "scenario": "Recall user name after unrelated turns",
        "turns": [
            "Tên tôi là Linh.",
            "Hôm nay tôi đang làm bài Lab 17.",
            "Memory agent cần có router.",
            "Tên tôi là gì?"
        ],
        "expected_keywords": ["Linh"],
        "category": "profile recall"
    },
    {
        "id": "case_04_profile_programming_language",
        "scenario": "Recall favorite programming language",
        "turns": [
            "My favorite programming language is Python.",
            "I am working on a benchmark script.",
            "What is my favorite programming language?"
        ],
        "expected_keywords": ["Python"],
        "category": "profile recall"
    },
    {
        "id": "case_05_episodic_previous_decision",
        "scenario": "Recall previous architecture decision",
        "turns": [
            "Kết luận: ta chọn JSON làm episodic memory để lưu project events.",
            "Sau đó ta sẽ viết benchmark.",
            "Hôm trước ta đã chọn gì cho episodic memory?"
        ],
        "expected_keywords": ["JSON", "episodic"],
        "category": "episodic recall"
    },
    {
        "id": "case_06_episodic_debug_lesson",
        "scenario": "Recall previous debug lesson",
        "turns": [
            "Bài học debug: khi chạy Docker Compose thì dùng docker service name thay vì localhost.",
            "Ta đã hoàn tất phần debug này.",
            "Previous debug lesson là gì?"
        ],
        "expected_keywords": ["docker", "service name"],
        "category": "episodic recall"
    },
    {
        "id": "case_07_semantic_benchmark_retrieval",
        "scenario": "Semantic retrieval for benchmark requirement",
        "turns": [
            "Benchmark should compare agents with memory and without memory over 10 multi-turn conversations.",
            "The report should include response relevance and token efficiency.",
            "What should benchmark compare?"
        ],
        "expected_keywords": ["memory", "without memory", "10"],
        "category": "semantic retrieval"
    },
    {
        "id": "case_08_semantic_token_budget",
        "scenario": "Semantic retrieval for token budget rule",
        "turns": [
            "Token budget management should trim low-priority messages first and keep the current query.",
            "Retrieved memory should be kept if relevant.",
            "What should token budget management keep?"
        ],
        "expected_keywords": ["current query", "memory"],
        "category": "trim/token budget"
    },
    {
        "id": "case_09_recent_context",
        "scenario": "Recent conversation recall",
        "turns": [
            "API chỉ làm nhiệm vụ transfer data.",
            "Tôi vừa nói gì về API?"
        ],
        "expected_keywords": ["transfer", "data"],
        "category": "recent context"
    },
    {
        "id": "case_10_full_stack_requirement",
        "scenario": "Semantic recall of full memory stack",
        "turns": [
            "Full memory stack includes short-term, profile, episodic, and semantic memory.",
            "Each backend must have separate save and retrieve logic.",
            "What are the four memory types?"
        ],
        "expected_keywords": ["short-term", "profile", "episodic", "semantic"],
        "category": "semantic retrieval"
    },
]
