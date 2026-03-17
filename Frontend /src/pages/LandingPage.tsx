import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Code2, Brain, MessageSquare, ArrowRight, Terminal, Sparkles, BarChart3 } from "lucide-react";
import { useNavigate } from "react-router-dom";

const features = [
  {
    icon: Code2,
    title: "Coding Interviews",
    description: "Practice algorithmic challenges with an AI interviewer. Supports Python, JavaScript, and C++.",
    color: "text-primary",
    bg: "bg-primary/10",
  },
  {
    icon: Brain,
    title: "System Design",
    description: "Design scalable systems with real-time AI follow-up questions and architecture analysis.",
    color: "text-info",
    bg: "bg-info/10",
  },
  {
    icon: MessageSquare,
    title: "Behavioral",
    description: "Sharpen your storytelling with STAR-method coaching and communication feedback.",
    color: "text-accent",
    bg: "bg-accent/10",
  },
];

const stats = [
  { value: "10K+", label: "Practice Sessions" },
  { value: "95%", label: "Satisfaction Rate" },
  { value: "3x", label: "Faster Improvement" },
  { value: "500+", label: "Questions" },
];

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="fixed top-0 w-full z-50 border-b border-border/50 bg-background/80 backdrop-blur-xl">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="h-6 w-6 text-primary" />
            <span className="font-heading text-xl font-bold">InterviewOS</span>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="ghost" onClick={() => navigate("/auth")}>Log in</Button>
            <Button onClick={() => navigate("/auth?mode=signup")}>Get Started</Button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 bg-hero opacity-[0.03]" />
        <div className="absolute top-20 right-10 w-72 h-72 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-10 left-10 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />
        
        <div className="container relative">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="max-w-3xl mx-auto text-center"
          >
            <div className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-sm text-primary mb-8">
              <Sparkles className="h-3.5 w-3.5" />
              AI-Powered Interview Practice
            </div>
            <h1 className="text-5xl md:text-7xl font-bold font-heading tracking-tight leading-[1.1] mb-6">
              Ace Your Next
              <span className="text-gradient block">Tech Interview</span>
            </h1>
            <p className="text-lg md:text-xl text-muted-foreground max-w-xl mx-auto mb-10 leading-relaxed">
              Practice coding, system design, and behavioral interviews with an AI interviewer that adapts to your skill level and provides real-time feedback.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="h-12 px-8 text-base font-semibold shadow-glow" onClick={() => navigate("/auth?mode=signup")}>
                Start Practicing Free
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button variant="outline" size="lg" className="h-12 px-8 text-base" onClick={() => navigate("/auth")}>
                View Demo
              </Button>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-2xl mx-auto"
          >
            {stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-3xl font-bold font-heading text-foreground">{stat.value}</div>
                <div className="text-sm text-muted-foreground mt-1">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 border-t border-border/50">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold font-heading mb-4">Three Interview Types, One Platform</h2>
            <p className="text-muted-foreground text-lg max-w-lg mx-auto">Master every aspect of the technical interview process with personalized AI coaching.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="group relative rounded-xl border border-border bg-card p-8 hover:shadow-lg transition-all duration-300 hover:border-primary/20"
              >
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg ${feature.bg} mb-5`}>
                  <feature.icon className={`h-6 w-6 ${feature.color}`} />
                </div>
                <h3 className="text-xl font-semibold font-heading mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-24 bg-secondary/30 border-t border-border/50">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold font-heading mb-4">How It Works</h2>
          </div>
          <div className="grid md:grid-cols-3 gap-12 max-w-4xl mx-auto">
            {[
              { step: "01", title: "Choose Interview Type", desc: "Select coding, system design, or behavioral based on what you want to practice." },
              { step: "02", title: "Practice with AI", desc: "The AI interviewer asks questions, provides follow-ups, and challenges your thinking." },
              { step: "03", title: "Get Detailed Feedback", desc: "Receive scores, improvement tips, and track your progress over time." },
            ].map((item, i) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="text-center"
              >
                <div className="text-5xl font-bold font-heading text-primary/20 mb-4">{item.step}</div>
                <h3 className="text-lg font-semibold font-heading mb-2">{item.title}</h3>
                <p className="text-muted-foreground">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 border-t border-border/50">
        <div className="container">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative max-w-3xl mx-auto text-center rounded-2xl bg-secondary p-12 md:p-16 overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-transparent" />
            <div className="relative">
              <BarChart3 className="h-10 w-10 text-primary mx-auto mb-6" />
              <h2 className="text-3xl md:text-4xl font-bold font-heading text-secondary-foreground mb-4">
                Ready to Level Up?
              </h2>
              <p className="text-secondary-foreground/70 text-lg mb-8 max-w-md mx-auto">
                Join thousands of engineers preparing for interviews at top tech companies.
              </p>
              <Button size="lg" className="h-12 px-8 text-base font-semibold shadow-glow" onClick={() => navigate("/auth?mode=signup")}>
                Start Your First Interview
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-8">
        <div className="container flex items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Terminal className="h-4 w-4 text-primary" />
            <span className="font-heading font-semibold text-foreground">InterviewOS</span>
          </div>
          <p>© 2026 InterviewOS. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
