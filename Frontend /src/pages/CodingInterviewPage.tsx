import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Editor from "@monaco-editor/react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Terminal, ArrowLeft, Send, Clock, Play, Loader2 } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const CODING_QUESTIONS = [
  { id: "two-sum", title: "Two Sum", difficulty: "Easy", description: "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1]." },
  { id: "lru-cache", title: "LRU Cache", difficulty: "Medium", description: "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.\n\nImplement the LRUCache class:\n- LRUCache(int capacity) Initialize the LRU cache with positive size capacity.\n- int get(int key) Return the value of the key if the key exists, otherwise return -1.\n- void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache." },
  { id: "merge-intervals", title: "Merge Intervals", difficulty: "Medium", description: "Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.\n\nExample:\nInput: intervals = [[1,3],[2,6],[8,10],[15,18]]\nOutput: [[1,6],[8,10],[15,18]]" },
];

const STARTER_CODE: Record<string, Record<string, string>> = {
  python: {
    "two-sum": 'def two_sum(nums, target):\n    # Your code here\n    pass',
    "lru-cache": 'class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n\n    def get(self, key: int) -> int:\n        pass\n\n    def put(self, key: int, value: int) -> None:\n        pass',
    "merge-intervals": 'def merge(intervals):\n    # Your code here\n    pass',
  },
  javascript: {
    "two-sum": 'function twoSum(nums, target) {\n  // Your code here\n}',
    "lru-cache": 'class LRUCache {\n  constructor(capacity) {\n    // Your code here\n  }\n  get(key) {\n    // Your code here\n  }\n  put(key, value) {\n    // Your code here\n  }\n}',
    "merge-intervals": 'function merge(intervals) {\n  // Your code here\n}',
  },
  cpp: {
    "two-sum": '#include <vector>\nusing namespace std;\n\nvector<int> twoSum(vector<int>& nums, int target) {\n    // Your code here\n}',
    "lru-cache": '#include <unordered_map>\n#include <list>\nusing namespace std;\n\nclass LRUCache {\npublic:\n    LRUCache(int capacity) {\n        // Your code here\n    }\n    int get(int key) {\n        // Your code here\n    }\n    void put(int key, int value) {\n        // Your code here\n    }\n};',
    "merge-intervals": '#include <vector>\n#include <algorithm>\nusing namespace std;\n\nvector<vector<int>> merge(vector<vector<int>>& intervals) {\n    // Your code here\n}',
  },
};

export default function CodingInterviewPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [selectedQuestion, setSelectedQuestion] = useState(CODING_QUESTIONS[0]);
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState(STARTER_CODE.python["two-sum"]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [timer, setTimer] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning) {
      interval = setInterval(() => setTimer(t => t + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  const handleQuestionChange = (qId: string) => {
    const q = CODING_QUESTIONS.find(q => q.id === qId)!;
    setSelectedQuestion(q);
    setCode(STARTER_CODE[language][qId] || "// Start coding here");
    setMessages([]);
  };

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang);
    setCode(STARTER_CODE[lang][selectedQuestion.id] || "// Start coding here");
  };

  const startInterview = () => {
    setIsRunning(true);
    setTimer(0);
    setMessages([{
      role: "assistant",
      content: `Welcome! Let's work on **${selectedQuestion.title}** (${selectedQuestion.difficulty}).\n\n${selectedQuestion.description}\n\nTake your time to think through the approach. When you're ready, explain your thinking or start coding. I'll ask follow-up questions along the way.`
    }]);
  };

  const sendMessage = async () => {
    if (!chatInput.trim()) return;
    const userMsg: Message = { role: "user", content: chatInput };
    setMessages(prev => [...prev, userMsg]);
    setChatInput("");
    setIsLoading(true);

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const responses = [
        "Good thinking! Can you walk me through the time complexity of your approach?",
        "That's a valid approach. Have you considered using a hash map to optimize the lookup?",
        "Interesting! What happens if the input array is empty? How would you handle edge cases?",
        "Nice progress! Can you think of a way to solve this in O(n) time?",
        "Great explanation. Now, what about the space complexity? Can we do better?",
      ];
      setMessages(prev => [...prev, {
        role: "assistant",
        content: responses[Math.floor(Math.random() * responses.length)]
      }]);
      setIsLoading(false);
    }, 1500);
  };

  const submitCode = () => {
    setIsLoading(true);
    setMessages(prev => [...prev, { role: "user", content: `[Submitted code for evaluation]\n\`\`\`${language}\n${code}\n\`\`\`` }]);

    setTimeout(() => {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: `## Code Review\n\nI've analyzed your submission for **${selectedQuestion.title}**.\n\n**Correctness:** 7/10\n**Time Complexity:** Could be optimized\n**Space Complexity:** Acceptable\n**Code Clarity:** 8/10\n\n### Feedback\nYour approach is on the right track. Consider:\n- Edge case handling for empty inputs\n- Using a hash map for O(n) lookup\n- Adding more descriptive variable names\n\n### Suggestion\nTry implementing the solution using a hash map to achieve O(n) time complexity.`
      }]);
      setIsLoading(false);
    }, 2000);
  };

  const monacoLang = language === "cpp" ? "cpp" : language === "python" ? "python" : "javascript";

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-background/80 backdrop-blur-xl z-50 shrink-0">
        <div className="flex h-14 items-center justify-between px-4">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={() => navigate("/dashboard")}>
              <ArrowLeft className="h-4 w-4 mr-1" /> Back
            </Button>
            <div className="h-6 w-px bg-border" />
            <Select value={selectedQuestion.id} onValueChange={handleQuestionChange}>
              <SelectTrigger className="w-48 h-8 text-sm">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {CODING_QUESTIONS.map(q => (
                  <SelectItem key={q.id} value={q.id}>
                    {q.title} ({q.difficulty})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={language} onValueChange={handleLanguageChange}>
              <SelectTrigger className="w-32 h-8 text-sm">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="python">Python</SelectItem>
                <SelectItem value="javascript">JavaScript</SelectItem>
                <SelectItem value="cpp">C++</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-sm text-muted-foreground font-mono">
              <Clock className="h-4 w-4" />
              {formatTime(timer)}
            </div>
            {!isRunning ? (
              <Button size="sm" onClick={startInterview}>
                <Play className="h-3.5 w-3.5 mr-1" /> Start Interview
              </Button>
            ) : (
              <Button size="sm" variant="destructive" onClick={submitCode}>
                Submit Code
              </Button>
            )}
          </div>
        </div>
      </header>

      {/* Main content */}
      <div className="flex-1 flex min-h-0">
        {/* Code editor */}
        <div className="flex-1 border-r border-border">
          <Editor
            height="100%"
            language={monacoLang}
            value={code}
            onChange={(v) => setCode(v || "")}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              fontFamily: "JetBrains Mono, monospace",
              padding: { top: 16 },
              lineNumbers: "on",
              scrollBeyondLastLine: false,
              automaticLayout: true,
            }}
          />
        </div>

        {/* Chat panel */}
        <div className="w-[400px] flex flex-col bg-card">
          <div className="px-4 py-3 border-b border-border text-sm font-semibold font-heading flex items-center gap-2">
            <Terminal className="h-4 w-4 text-primary" />
            AI Interviewer
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-muted-foreground text-sm mt-20">
                <Terminal className="h-8 w-8 mx-auto mb-3 opacity-30" />
                Click "Start Interview" to begin your coding session.
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[85%] rounded-xl px-4 py-3 text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-foreground"
                }`}>
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-muted rounded-xl px-4 py-3">
                  <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
          <div className="p-3 border-t border-border">
            <div className="flex gap-2">
              <input
                value={chatInput}
                onChange={e => setChatInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && !e.shiftKey && sendMessage()}
                placeholder={isRunning ? "Explain your approach..." : "Start the interview first"}
                disabled={!isRunning}
                className="flex-1 rounded-lg border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
              />
              <Button size="icon" onClick={sendMessage} disabled={!isRunning || !chatInput.trim()}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
