"""Edit this file, then run:  python scripts/build.py
Everything in the README and the SVG cards comes from here."""

GITHUB_USER = "ZoolCoder"   # <-- your GitHub username (profile repo must be named the same)
BRAND = "ZoolCoder"
NAME = "Abdallah Emad"
NAME_AR = "عبدالله عماد"
TAGLINE = "Arabic-first, offline-first software · coding since 2005"

PORTFOLIO = "https://zoolcoder.com"
PHOTO = "assets/me.jpg"  # front-facing photo, used for the ASCII portrait

# hero HUD readouts
SINCE = 2005
PRO_SINCE = 2012
AI_SINCE = 2023
NOW = ["AI agents", "UAE e-invoicing", "Project tracker", "3D museum"]

# rotating lines under the name in the hero
TYPING_LINES = [
    "Spring Boot · Vue 3 · Flutter",
    "Building Arabic-first apps for Sudan and the Gulf",
    "Offline-first, because the network isn't guaranteed",
    "Coding since 2005 · professional since 2012",
    "Government-scale Java, cloud-native full stack",
    "AI champion since 2023: AI woven into every step",
    "Open for projects · zoolcoder.com",
]

# spec sheet next to the portrait: (label, value)
INFO = [
    ("Studio", "ZoolCoder"),
    ("Founder", "Abdallah Emad"),
    ("Coding since", "2005  ·  pro since 2012"),
    ("Backend", "Spring Boot 4, Java 21, Go, GraalVM"),
    ("Distributed", "Microservices, Kafka, Spring Cloud"),
    ("Web", "Vue 3, Quasar, React, TypeScript"),
    ("Mobile", "Flutter, Riverpod, Dart"),
    ("Data", "PostgreSQL, pgvector, Redis, Oracle"),
    ("3D / XR", "Babylon.js, Three.js, WebXR"),
    ("Cloud", "Cloudflare Workers, AWS, GCP"),
    ("DevOps", "Docker, Kubernetes, Jenkins, GitLab"),
    ("AI", "Champion since 2023 · agents, LLMs, MCP"),
    ("Focus", "Offline-first, RTL, AI features"),
    ("In production", "Many live products"),
]

ABOUT = [
    "🚀 Writing code since **2005**. Today **ZoolCoder** builds Arabic-first, right-to-left, offline-first products.",
    "🏛️ Professional since 2012: national e-passport and civil-registration platforms, ID-document systems for government programmes, enterprise microservices and cloud-native full stack.",
    "🤖 **AI champion & engineer since 2023**: I integrate LLMs, coding agents, MCP tools and on-device ML into the whole flow, from spec to review to release, and into the products themselves.",
    "☁️ AWS Certified Developer and Google Cloud Associate Cloud Engineer (2023).",
    "🧩 One engineer end to end: Spring Boot backends, Vue web apps, Flutter mobile, 3D on the web.",
    "🟢 Many products running live in production across web, mobile, POS and 3D. Product names stay private; a few are outlined below.",
    "🛠️ Currently: AI agents in the build pipeline, UAE e-invoicing for a POS platform, a self-hosted project tracker, and a 3D web museum.",
]

# product names stay private: cards show only what kind of system it is
# status: LIVE | ACTIVE | SHIPPED  (drives the chip colour on each card)
PROJECTS = [
    dict(name="3D Web Museum", icon="🏛️", ar="", status="LIVE", link="",
         desc="Trilingual 3D museum in the browser: seven historical eras, guided WebXR shows.",
         tags=["Babylon.js", "Three.js", "WebXR"]),
    dict(name="Offline-first POS", icon="🧾", ar="", status="ACTIVE", link="",
         desc="Point of sale that keeps selling without network: fiscalisation, card terminals, e-invoicing.",
         tags=["Flutter", "Spring Boot", "Event sourcing"]),
    dict(name="Ticketing Marketplace", icon="🚌", ar="", status="LIVE", link="",
         desc="Intercity bus-ticket marketplace with payment verification read from banking screenshots.",
         tags=["Spring Boot", "OCR", "PostgreSQL"]),
    dict(name="On-device Payment OCR", icon="📸", ar="", status="LIVE", link="",
         desc="Merchants snap a banking screenshot and the payment is verified on the device, offline.",
         tags=["Flutter", "ML Kit", "Supabase"]),
    dict(name="Social Deduction Game", icon="🐺", ar="", status="LIVE", link="",
         desc="Party game with a rules engine validated over 5,000 simulated games.",
         tags=["Dart", "Flutter", "Riverpod"]),
    dict(name="Classic Games + AI", icon="🎲", ar="", status="LIVE", link="",
         desc="Traditional board games, played against a minimax AI opponent.",
         tags=["Flutter", "Hive", "Game AI"]),
]

# career timeline: (year, icon, title, detail). No employer or client names.
TIMELINE = [
    ("2005", "💻", "First code", "Self-taught, building since school"),
    ("2012", "🏛️", "Gov platforms", "e-passport portal, civil registry hub, BI"),
    ("2015", "🧪", "Quality eng.", "Selenium automation, test strategy"),
    ("2017", "🪪", "ID-doc systems", "Java EE microservices, Kubernetes"),
    ("2023", "🤖", "AI + cloud", "AI champion, LLM agents, AWS/GCP"),
    ("NOW", "🚀", "ZoolCoder", "Arabic-first, AI-native, many live"),
]

# how AI runs through the delivery flow: (icon, step, detail)
AI_FLOW = [
    ("💡", "Idea", "prompt-driven specs"),
    ("📐", "Plan", "AI-drafted design"),
    ("🤖", "Agents", "LLM pair-programming"),
    ("🧪", "Test", "generated test suites"),
    ("🔍", "Review", "automated code review"),
    ("🚀", "Ship", "AI features in product"),
]
AI_HUB = 2  # index of the highlighted step

# headline numbers under the hero
METRICS = [
    ("2005", "first line of code"),
    ("14+ yrs", "professional engineering"),
    ("Gov-scale", "e-passport & ID systems"),
    ("AWS + GCP", "cloud certified"),
    ("Many", "products live today"),
]

# what ZoolCoder sells: (icon, title, pitch)
SERVICES = [
    ("🤖", "AI integration", "LLM features, agents, RAG and MCP tools inside your product and your team's delivery flow."),
    ("🏢", "Enterprise backends", "Java 21 / Spring Boot 4 and Go services, contract-first APIs, microservices, Kafka."),
    ("🌍", "Arabic-first products", "RTL-native web and mobile apps, trilingual content, built for MENA users."),
    ("📱", "Offline-first mobile & POS", "Flutter apps that keep working without network and sync when it returns."),
    ("⚡", "Edge & cloud", "Cloudflare Workers, AWS and Google Cloud: fast, cheap to run, observable."),
    ("🧊", "3D & WebXR", "Interactive 3D sites and immersive WebXR experiences that run in the browser."),
]

# the full toolbox, grouped: shown as chips under the icons
ARSENAL = {
    "AI": ["Claude Code", "LLM agents", "MCP servers", "RAG + pgvector", "Workers AI", "ML Kit on-device"],
    "Backend": ["Java 21", "Spring Boot 4", "Hibernate/JPA", "Flyway", "MapStruct", "Go", "sqlc + pgx", "gRPC", "Kafka"],
    "API": ["OpenAPI contract-first", "oapi-codegen", "OAuth2 / OIDC", "Zitadel", "Keycloak"],
    "Web": ["Vue 3", "Quasar", "Pinia", "TypeScript", "Vite / vite-ssg", "Tailwind", "TipTap", "ECharts", "GSAP", "Hono", "Zod"],
    "Mobile": ["Flutter", "Riverpod", "Drift", "go_router", "Dio", "Supabase"],
    "Data": ["PostgreSQL", "PostGIS", "pgvector", "Redis", "Meilisearch", "Oracle", "Cloudflare D1 / R2", "Neon"],
    "Ops": ["Docker", "Kubernetes", "Traefik", "Prometheus", "Grafana", "GitLab CI", "Jenkins", "Cloud Run"],
    "Quality": ["Vitest", "Playwright", "axe-core", "JUnit 5", "Testcontainers", "golangci-lint", "Selenium"],
}

CTA = "Have a product to build or AI to bring into your flow?"

# skillicons.dev ids
SKILLS = {
    "Languages": "java,kotlin,go,ts,js,dart,python",
    "Backend": "spring,hibernate,gradle,nodejs,kafka",
    "Frontend": "vue,pinia,vite,react,tailwind,threejs",
    "Mobile": "flutter,androidstudio",
    "Data": "postgres,mysql,redis,supabase,sqlite",
    "Cloud": "cloudflare,aws,gcp",
    "DevOps": "docker,kubernetes,grafana,prometheus,gitlab,githubactions,jenkins,linux",
    "Testing": "vitest,selenium",
}
