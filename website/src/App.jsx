const portfolioItems = [
  {
    id: 1,
    company: "TRMW Sports",
    role: "Cloud Engineer",
    project: "TGL Golf - ScoreSight",
    period: "2023 – Present",
    description:
      "Designed and maintained cloud infrastructure for ScoreSight, TGL Golf's real-time scoring and broadcast data platform. Architected serverless pipelines on AWS to ingest, process, and deliver live scoring data with low latency to global audiences.",
    tags: ["AWS", "Serverless", "Real-time Data", "CDK"],
  },
  {
    id: 2,
    company: "Goldman Sachs",
    role: "Cloud Engineer",
    project: "Apple Card & Apple Savings",
    period: "2021 – 2023",
    description:
      "Supported cloud infrastructure for Apple's consumer financial products, including Apple Card and Apple Savings Account, in partnership with Goldman Sachs. Focused on scalable, secure, and compliant cloud architectures meeting strict financial-industry standards.",
    tags: ["AWS", "FinTech", "Compliance", "Terraform"],
  },
  {
    id: 3,
    company: "USCIS",
    role: "Backend Developer",
    project: "Immigration Systems Modernization",
    period: "2020 – 2021",
    description:
      "Developed backend services and APIs supporting USCIS digital transformation efforts. Built RESTful microservices to modernize legacy immigration processing systems, improving reliability and throughput for high-volume case workloads.",
    tags: ["Java", "Spring Boot", "REST APIs", "Microservices"],
  },
  {
    id: 4,
    company: "GSA",
    role: "Full Stack Developer",
    project: "SBA.gov",
    period: "2017 – 2020",
    description:
      "Built and maintained full-stack features for SBA.gov as part of the General Services Administration's digital services team. Delivered accessible, responsive web experiences helping small businesses access federal resources and funding information.",
    tags: ["React", "Node.js", "Accessibility", "Federal Web"],
  },
  {
    id: 5,
    company: "OMB",
    role: "Full Stack Developer",
    project: "ITDashboard.gov",
    period: "2014 – 2018",
    description:
      "Contributed full-stack development on ITDashboard.gov, the federal IT investment tracking portal for the Office of Management and Budget. Built data visualization features enabling OMB analysts and the public to monitor federal IT spending and project performance.",
    tags: ["React", "D3.js", "Python", "Data Visualization"],
  },
];

function HeroSection() {
  return (
    <section className="max-w-3xl mx-auto px-6 pt-20 pb-16">
      <p className="text-sm font-semibold tracking-widest text-sky-400 uppercase mb-4">
        Hello, I'm
      </p>
      <h1 className="text-5xl sm:text-6xl font-bold text-white mb-6 leading-tight">
        Diego
      </h1>
      <div className="w-12 h-1 bg-sky-500 rounded mb-8" />
      <p className="text-lg text-slate-300 leading-relaxed">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque
        vehicula augue vitae libero tincidunt, eget tincidunt nunc fermentum.
        Integer at metus non enim lacinia lacinia at sit amet ante. Praesent
        commodo cursus magna, vel scelerisque nisl consectetur et. Donec sed
        odio dui. Cras mattis consectetur purus sit amet fermentum.
      </p>
    </section>
  );
}

function PortfolioCard({ item }) {
  return (
    <article className="relative border border-slate-700 rounded-2xl p-6 sm:p-8 bg-slate-800/50 hover:border-sky-500/60 hover:bg-slate-800 transition-all duration-300 group">
      {/* top row */}
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 mb-3">
        <div>
          <h3 className="text-xl font-bold text-white group-hover:text-sky-300 transition-colors">
            {item.company}
          </h3>
          <p className="text-sky-400 text-sm font-medium mt-0.5">{item.role}</p>
        </div>
        <span className="text-slate-500 text-sm whitespace-nowrap">{item.period}</span>
      </div>

      {/* project badge */}
      <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider mb-4">
        {item.project}
      </p>

      {/* description */}
      <p className="text-slate-300 text-sm leading-relaxed mb-5">
        {item.description}
      </p>

      {/* tech tags */}
      <div className="flex flex-wrap gap-2">
        {item.tags.map((tag) => (
          <span
            key={tag}
            className="px-3 py-1 rounded-full text-xs font-medium bg-sky-950 text-sky-300 border border-sky-800"
          >
            {tag}
          </span>
        ))}
      </div>
    </article>
  );
}

function PortfolioSection() {
  return (
    <section className="max-w-3xl mx-auto px-6 pb-24">
      <h2 className="text-2xl font-bold text-white mb-2">Experience</h2>
      <div className="w-8 h-0.5 bg-sky-500 rounded mb-10" />
      <div className="flex flex-col gap-6">
        {portfolioItems.map((item) => (
          <PortfolioCard key={item.id} item={item} />
        ))}
      </div>
    </section>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <HeroSection />
      <PortfolioSection />
    </div>
  );
}
