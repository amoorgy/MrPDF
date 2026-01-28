import { Button } from "@/components/ui/button";
import { FileText, Upload, MessageSquare, Zap } from "lucide-react";
import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="h-6 w-6 text-primary" />
            <span className="text-xl font-semibold text-foreground">Mr PDF</span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/auth">
              <Button variant="ghost" size="sm">
                Sign in
              </Button>
            </Link>
            <Link to="/auth?mode=signup">
              <Button size="sm">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-24 text-center">
        <div className="max-w-3xl mx-auto space-y-8">
          <h1 className="text-5xl md:text-6xl font-serif font-semibold text-foreground leading-tight">
            Your documents,
            <br />
            <span className="text-muted">understood.</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-xl mx-auto">
            Upload any document. Ask anything. Get intelligent responses. 
            Mr PDF transforms how you interact with PDFs, Word docs, and more.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link to="/auth?mode=signup">
              <Button size="lg" className="w-full sm:w-auto">
                Start for free
              </Button>
            </Link>
            <Link to="#features">
              <Button variant="outline" size="lg" className="w-full sm:w-auto">
                Learn more
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="container mx-auto px-6 py-20">
        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <FeatureCard
            icon={Upload}
            title="Any Document"
            description="PDF, Word, PowerPoint, Excel — upload any supported format and start conversing."
          />
          <FeatureCard
            icon={MessageSquare}
            title="Natural Conversation"
            description="Ask questions in plain language. Get clear, contextual answers from your documents."
          />
          <FeatureCard
            icon={Zap}
            title="Instant Insights"
            description="Extract key information, summarize content, or find specific details in seconds."
          />
        </div>
      </section>

      {/* Pricing */}
      <section className="container mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-serif font-semibold text-foreground mb-4">
            Simple pricing
          </h2>
          <p className="text-muted-foreground">
            Start free, upgrade when you need more.
          </p>
        </div>
        <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          <PricingCard
            title="Free"
            price="$0"
            description="Perfect for getting started"
            features={["5 documents per month", "Basic AI responses", "Standard support"]}
          />
          <PricingCard
            title="Pro"
            price="$5"
            period="/month"
            description="For power users"
            features={["Unlimited documents", "Advanced AI features", "Priority support", "Export capabilities"]}
            highlighted
          />
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 mt-20">
        <div className="container mx-auto px-6 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-muted" />
              <span className="text-sm text-muted-foreground">Mr PDF</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2024 Mr PDF. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

const FeatureCard = ({
  icon: Icon,
  title,
  description,
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  description: string;
}) => (
  <div className="p-6 bg-card border border-border/50 space-y-4">
    <div className="w-10 h-10 bg-secondary flex items-center justify-center">
      <Icon className="h-5 w-5 text-secondary-foreground" />
    </div>
    <h3 className="font-semibold text-foreground">{title}</h3>
    <p className="text-sm text-muted-foreground">{description}</p>
  </div>
);

const PricingCard = ({
  title,
  price,
  period,
  description,
  features,
  highlighted,
}: {
  title: string;
  price: string;
  period?: string;
  description: string;
  features: string[];
  highlighted?: boolean;
}) => (
  <div
    className={`p-8 border ${
      highlighted
        ? "bg-primary text-primary-foreground border-primary"
        : "bg-card border-border/50"
    }`}
  >
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <div className="flex items-baseline gap-1 mb-2">
      <span className="text-3xl font-bold">{price}</span>
      {period && <span className="text-sm opacity-80">{period}</span>}
    </div>
    <p className={`text-sm mb-6 ${highlighted ? "opacity-80" : "text-muted-foreground"}`}>
      {description}
    </p>
    <ul className="space-y-3">
      {features.map((feature, i) => (
        <li key={i} className="text-sm flex items-center gap-2">
          <span className={highlighted ? "opacity-80" : "text-muted-foreground"}>✓</span>
          {feature}
        </li>
      ))}
    </ul>
    <Link to="/auth?mode=signup" className="block mt-6">
      <Button
        variant={highlighted ? "secondary" : "default"}
        className="w-full"
      >
        Get started
      </Button>
    </Link>
  </div>
);

export default Landing;
