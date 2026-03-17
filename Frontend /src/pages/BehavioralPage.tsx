import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Terminal, ArrowLeft, Send, Clock, Play, Loader2 } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const BEHAVIORAL_QUESTIONS = [
  "Tell me about a time you resolved a conflict in your team.",
  "Describe a challenging project you led from start to finish.",
  "Tell me about a time you had to make a difficult technical decision.",
  "Describe a situation where you had to learn something new quickly.",
];

export default function BehavioralPage() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [timer, setTimer] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [selectedQ, setSelectedQ] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning) interval = setInterval(() => setTimer(t => t + 1), 1000);
    return () => clearInterval(interval);
  }, [isRunning]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const formatTime = (s: number) => `${Math.floor(s / 60).toString().padStart(2, "0")}:${(s % 60).toString().padStart(2, "0")}`;

  const startInterview = (q: string) => {
    setSelectedQ(q);
    setIsRunning(true);
    setTimer(0);
    setMessages([{
      role: "assistant",
      content: `Let's begin the behavioral interview.\n\n**${q}**\n\nTake a moment to think, then walk me through the situation using the STAR method:\n- **Situation:** Set the context\n- **Task:** What was your responsibility?\n- **Action:** What did you do?\n- **Result:** What was the outcome?\n\nGo ahead whenever you're ready.`
    }]);
  };

  const sendMessage = async () => {
    if (!chatInput.trim()) return;
    setMessages(prev => [...prev, { role: "user", content: chatInput }]);
    setChatInput("");
    setIsLoading(true);

    setTimeout(() => {
      const followUps = [
        "Thank you for sharing that. Can you elaborate on what specific actions *you* personally took in that situation?",
        "Interesting! What did you learn from this experience? How has it changed your approach going forward?",
        "Good detail. How did your team react to your approach? Was there any pushback?",
        "That's a solid example. Can you quantify the impact? What metrics improved as a result?",
        "Great context. What would you do differently if you faced the same situation today?",
      ];
      setMessages(prev => [...prev, {
        role: "assistant",
        content: followUps[Math.floor(Math.random() * followUps.length)]
      }]);
      setIsLoading(false);
    }, 1500);
  };

  const endInterview = () => {
    setIsRunning(false);
    setMessages(prev => [...prev, {
      role: "assistant",
      content: `## Behavioral Interview Evaluation\n\n**Communication Clarity:** 7/10\n**Structured Thinking (STAR):** 6/10\n**Leadership Evidence:** 7/10\n**Problem Solving:** 8/10\n**Self-Awareness:** 7/10\n\n### Strengths\n- Clear and concise communication\n- Good situational awareness\n\n### Areas for Improvement\n- Structure your answer more tightly around the STAR framework\n- Quantify results with specific metrics\n- Show more of your personal contribution vs. the team's\n\n### Tips\n- Prepare 5-7 stories that cover different competencies\n- Practice the 2-minute version of each story\n- Always end with measurable results`
    }]);
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <header className="border-b border-border/50 bg-background/80 backdrop-blur-xl z-50 shrink-0">
        <div className="flex h-14 items-center justify-between px-4">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={() => navigate("/dashboard")}>
              <ArrowLeft className="h-4 w-4 mr-1" /> Back
            </Button>
            {selectedQ && (
              <>
                <div className="h-6 w-px bg-border" />
                <span className="text-sm font-medium truncate max-w-md">{selectedQ}</span>
              </>
            )}
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-sm text-muted-foreground font-mono">
              <Clock className="h-4 w-4" />
              {formatTime(timer)}
            </div>
            {isRunning && (
              <Button size="sm" variant="destructive" onClick={endInterview}>End Interview</Button>
            )}
          </div>
        </div>
      </header>

      <div className="flex-1 flex flex-col max-w-3xl mx-auto w-full min-h-0">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {!isRunning && messages.length === 0 && (
            <div className="mt-20">
              <h2 className="text-2xl font-bold font-heading text-center mb-2">Behavioral Interview</h2>
              <p className="text-muted-foreground text-center mb-8">Choose a question to begin practicing.</p>
              <div className="grid gap-4 max-w-lg mx-auto">
                {BEHAVIORAL_QUESTIONS.map(q => (
                  <button
                    key={q}
                    onClick={() => startInterview(q)}
                    className="text-left rounded-xl border border-border bg-card p-6 hover:border-primary/20 hover:shadow-md transition-all"
                  >
                    <p className="font-medium text-sm">{q}</p>
                  </button>
                ))}
              </div>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[80%] rounded-xl px-4 py-3 text-sm leading-relaxed ${
                msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-foreground"
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

        {isRunning && (
          <div className="p-4 border-t border-border">
            <div className="flex gap-2">
              <input
                value={chatInput}
                onChange={e => setChatInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && !e.shiftKey && sendMessage()}
                placeholder="Share your experience..."
                className="flex-1 rounded-lg border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              />
              <Button size="icon" onClick={sendMessage} disabled={!chatInput.trim()}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
