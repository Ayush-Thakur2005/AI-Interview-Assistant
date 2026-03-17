import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Terminal, ArrowLeft, Send, Clock, Play, Loader2 } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const DESIGN_PROMPTS = [
  "Design a URL shortener like bit.ly",
  "Design a Twitter-like social media feed",
  "Design a ride-sharing system like Uber",
  "Design a real-time chat application",
];

export default function SystemDesignPage() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [timer, setTimer] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [selectedPrompt, setSelectedPrompt] = useState("");
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

  const startInterview = (prompt: string) => {
    setSelectedPrompt(prompt);
    setIsRunning(true);
    setTimer(0);
    setMessages([{
      role: "assistant",
      content: `Great, let's begin the system design interview.\n\n**${prompt}**\n\nBefore diving into the design, let's start with requirements:\n\n1. What are the core features you'd prioritize?\n2. What scale are we designing for? (DAU, requests/sec)\n3. Are there any specific constraints?\n\nTake a moment to clarify requirements, then walk me through your high-level architecture.`
    }]);
  };

  const sendMessage = async () => {
    if (!chatInput.trim()) return;
    setMessages(prev => [...prev, { role: "user", content: chatInput }]);
    setChatInput("");
    setIsLoading(true);

    setTimeout(() => {
      const followUps = [
        "Good point! Now, how would you handle a sudden spike in traffic? What happens when your primary database becomes a bottleneck?",
        "Interesting approach. What caching strategy would you use? Where would you place the cache in your architecture?",
        "That makes sense. How would you handle data consistency across multiple services? Would you use eventual consistency or strong consistency?",
        "Nice! Let's talk about the database design. What type of database would you choose and why? How would you shard the data?",
        "Great consideration! What about failure scenarios? How does your system handle a node going down? What's your failover strategy?",
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
      content: `## System Design Evaluation\n\n**Architecture Clarity:** 7/10\n**Scalability:** 6/10\n**Database Design:** 7/10\n**Caching Strategy:** 5/10\n**Trade-off Analysis:** 8/10\n\n### Strengths\n- Good understanding of high-level architecture\n- Solid requirement clarification\n\n### Areas for Improvement\n- Consider more specific caching strategies (Redis, CDN)\n- Discuss load balancing approaches\n- Address data partitioning in more detail\n\n### Recommended Study\n- Read about consistent hashing\n- Study CAP theorem applications\n- Practice drawing architecture diagrams`
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
            {selectedPrompt && (
              <>
                <div className="h-6 w-px bg-border" />
                <span className="text-sm font-medium">{selectedPrompt}</span>
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
              <h2 className="text-2xl font-bold font-heading text-center mb-2">System Design Interview</h2>
              <p className="text-muted-foreground text-center mb-8">Choose a design prompt to begin.</p>
              <div className="grid sm:grid-cols-2 gap-4">
                {DESIGN_PROMPTS.map(prompt => (
                  <button
                    key={prompt}
                    onClick={() => startInterview(prompt)}
                    className="text-left rounded-xl border border-border bg-card p-6 hover:border-primary/20 hover:shadow-md transition-all"
                  >
                    <p className="font-medium text-sm">{prompt}</p>
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
                placeholder="Describe your architecture approach..."
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
