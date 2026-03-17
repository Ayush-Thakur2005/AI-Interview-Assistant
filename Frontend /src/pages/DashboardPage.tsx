import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/useAuth";
import { Terminal, Code2, Brain, MessageSquare, BarChart3, Clock, Trophy, LogOut, ChevronRight } from "lucide-react";

const interviewTypes = [
  {
    id: "coding",
    title: "Coding Interview",
    description: "Algorithmic problems with AI evaluation",
    icon: Code2,
    color: "text-primary",
    bg: "bg-primary/10",
    route: "/interview/coding",
  },
  {
    id: "system-design",
    title: "System Design",
    description: "Architecture discussions with follow-ups",
    icon: Brain,
    color: "text-info",
    bg: "bg-info/10",
    route: "/interview/system-design",
  },
  {
    id: "behavioral",
    title: "Behavioral",
    description: "STAR method coaching and feedback",
    icon: MessageSquare,
    color: "text-accent",
    bg: "bg-accent/10",
    route: "/interview/behavioral",
  },
];

const mockStats = [
  { label: "Interviews Completed", value: "0", icon: Trophy },
  { label: "Practice Hours", value: "0", icon: Clock },
  { label: "Avg Score", value: "—", icon: BarChart3 },
];

export default function DashboardPage() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-background/80 backdrop-blur-xl sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate("/")}>
            <Terminal className="h-6 w-6 text-primary" />
            <span className="font-heading text-xl font-bold">InterviewOS</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">{user?.email}</span>
            <Button variant="ghost" size="sm" onClick={handleSignOut}>
              <LogOut className="h-4 w-4 mr-1" /> Sign Out
            </Button>
          </div>
        </div>
      </header>

      <main className="container py-10">
        {/* Welcome */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-10">
          <h1 className="text-3xl font-bold font-heading mb-2">
            Welcome back{user?.user_metadata?.full_name ? `, ${user.user_metadata.full_name}` : ""}
          </h1>
          <p className="text-muted-foreground">Choose an interview type to start practicing.</p>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
          {mockStats.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="rounded-xl border border-border bg-card p-6"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <stat.icon className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="text-2xl font-bold font-heading">{stat.value}</p>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Interview Types */}
        <h2 className="text-xl font-bold font-heading mb-6">Start a Practice Interview</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {interviewTypes.map((type, i) => (
            <motion.div
              key={type.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + i * 0.1 }}
              onClick={() => navigate(type.route)}
              className="group cursor-pointer rounded-xl border border-border bg-card p-8 hover:shadow-lg hover:border-primary/20 transition-all duration-300"
            >
              <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg ${type.bg} mb-5`}>
                <type.icon className={`h-6 w-6 ${type.color}`} />
              </div>
              <h3 className="text-lg font-semibold font-heading mb-2">{type.title}</h3>
              <p className="text-muted-foreground text-sm mb-4">{type.description}</p>
              <div className="flex items-center text-primary text-sm font-medium group-hover:gap-2 transition-all">
                Start Interview <ChevronRight className="h-4 w-4 ml-1" />
              </div>
            </motion.div>
          ))}
        </div>
      </main>
    </div>
  );
}
