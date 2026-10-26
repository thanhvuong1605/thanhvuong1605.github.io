// Terminal commands and their outputs
const commands = {
    about: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">About Me</p>
                <p>Senior Data Scientist and Machine Learning Engineer Lead with years of experience building real-time ML systems for ride-hailing, e-commerce, and fintech platforms.</p>
            </div>
            <div class="block">
                <p>Graduated with a Master of Artificial Intelligence from RMIT University in 2026 (Distinction, scholarship), where my GuideFlow capstone with AstraZeneca won the Best Project Award. Led ML teams and shipped models that drive revenue, improve conversion, and optimize operations at scale.</p>
            </div>
            <div class="block">
                <p class="section-title" style="color: #e86464;">What I Do</p>
                <p>I specialize in designing and deploying production ML systems that solve real-world problems at scale. My work spans dynamic pricing algorithms, recommendation systems, search optimization, and real-time prediction models.</p>
            </div>
            <div class="block">
                <p>I'm passionate about building AI systems that are not just technically sophisticated, but also deliver measurable business impact and improve user experiences.</p>
            </div>
        </div>
    `,
    
    experience: `
        <div class="command-output">
            <div class="block">
                <p>Type a company name to see detailed experience:</p>
                <div class="nav-links" style="margin-top: 1.5rem;">
                    <a href="#" data-command="masterhive">masterhive</a>
                    <a href="#" data-command="be">be</a>
                    <a href="#" data-command="sendo">sendo</a>
                    <a href="#" data-command="fpt">fpt</a>
                    <a href="#" data-command="volunteer">volunteer</a>
                    <a href="#" data-command="other">other</a>
                </div>
            </div>
        </div>
    `,
    
    be: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Be Group JSC - Ride-hailing Application</p>
                <p><i>Senior Data Scientist/Machine Learning Engineer Lead</i> | 08/2022 - 09/2026</p>
            </div>
            
            <div class="block">
                <p style="margin-top: 1.5rem;">Led a team of 4 ML engineers to design and maintain real-time ML models for pricing, dispatch, and recommendations, car pool and delivery systems. Developed and optimized production ML pipelines, improving scalability and efficiency.</p>
            </div>

            <div class="block">
                <p class="section-title" style="color: #e86464;">Key Projects:</p>
            </div>

            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Internal AI Agent Platform</p>
                <ul>
                    <li>Designed and built an <strong>internal multi-agent AI platform</strong> giving the DS &amp; engineering teams a unified assistant for daily knowledge work</li>
                    <li>Use cases: Q&amp;A over <strong>Confluence docs, GitLab code, and BigQuery datasets</strong>; dispatch rule configuration &amp; explanation; on-call troubleshooting and operational support</li>
                    <li>Built an <strong>internal MCP server</strong> bridging agents to Confluence, GitLab, and BigQuery, so any agent can answer with grounded company knowledge</li>
                    <li>Delivered a <strong>Dispatch configuration UI</strong> on top: business team configures dispatch scoring rules via web UI; AI explains rule impact (trace driver, simulate, estimate). Rule changes <strong>hot-reload into the production dispatch engine</strong> in real time, replacing ad-hoc code-edit-and-deploy workflows</li>
                </ul>
            </div>

            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Dynamic Pricing Engine</p>
                <ul>
                    <li>Designed and implemented a surge pricing model, increasing revenue by <strong>70-100%</strong> during peak hours and rainy conditions</li>
                    <li>Developed a demand-supply forecasting model to predict market conditions for the next 30 minutes (6 time steps)</li>
                    <li>Built a pricing engine that dynamically adjusts surge factors based on predicted demand and supply, optimizing balance in future time steps</li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Dispatch Engine</p>
                <ul>
                    <li>Built an <strong>A/B testing framework</strong> to validate dispatch strategies and model improvements in real-time production environments</li>
                    <li>Developed an enhanced driver–rider scoring model that increased <strong>completion rate (CR) by an additional 6%</strong> compared to the baseline model</li>
                    <li>Implemented a <strong>Multi-Armed Bandit (MAB)</strong> testing module to dynamically allocate traffic across dispatch policies, accelerating learning under changing market conditions</li>
                    <li>Implemented a linear sum assignment algorithm to maximize overall rider-driver match scores; reduced <strong>average pickup distance by 30%</strong></li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Food Recommendation Systems</p>
                <ul>
                    <li>Developed a hybrid recommendation model combining content-based filtering and collaborative filtering</li>
                    <li>Implemented a DeepFM model, improving ranking <strong>NDCG by 20%</strong> and achieving a <strong>15% increase in CTR</strong> through A/B testing</li>
                    <li>Recommendation engine contributes <strong>20% of food product traffic revenue</strong></li>
                    <li>Applied byte-pair encoding for Vietnamese tokenization in the food domain</li>
                    <li>Designed a keyword extraction model that analyzes user interactions to recommend relevant dishes</li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Be Search Engine - Food and Map Search</p>
                <ul>
                    <li>Architected the search systems for <strong>beMap</strong> and <strong>beFood</strong></li>
                    <li>Designed search logic optimized for business objectives, ranking items based on rating, partnerships, distance, and relevance</li>
                    <li>Developed a keyword suggestion feature using Elasticsearch, ranking terms dynamically via exponential moving average (EMA)</li>
                    <li>Search system drives <strong>60% of total food product traffic revenue</strong></li>
                    <li>Enabled real-time data synchronization</li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Additional Projects</p>
                <ul>
                    <li><strong>Waiting Time Estimation Model</strong> - Built predictive model to estimate driver waiting times within geofenced areas</li>
                    <li><strong>Food Delivery ETA Model</strong> - Designed predictive model for estimating delivery time ranges, improving <strong>on-time delivery rate by 50%</strong></li>
                    <li><strong>Dropoff Recommendation System</strong> - Developed model predicting user drop-off locations, with <strong>80% of users adopting</strong> the feature</li>
                </ul>
            </div>
        </div>
    `,

    masterhive: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">MasterHive.AI — Health-Data Platform Startup</p>
                <p><i>Founding Member</i> | 2026 - Present</p>
            </div>

            <div class="block">
                <p style="margin-top: 1.5rem;">Built a health-data platform from first design to a live system serving a province-scale user base. Three products:</p>
            </div>

            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">MasterHive — Electronic Health Record Platform</p>
                <ul>
                    <li>EHR for healthcare providers, in production across a provincial network of <strong>hospitals, district health centers and commune clinics</strong></li>
                    <li>Clinicians create, sign and manage records through configurable clinical forms, with each patient's history aggregated across facilities</li>
                </ul>
            </div>

            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">MasterFlow — Provincial Health Database Platform</p>
                <ul>
                    <li>Ingests and standardizes health-examination records from every facility in a province, enforces <strong>data-quality validation</strong>, and routes them through approval</li>
                    <li>Serves as the province's <strong>single reporting channel</strong> to the national Ministry of Health</li>
                    <li>In its first production deployment inside a <strong>government data center</strong> on a <strong>.gov.vn</strong> domain, with a partner API opening for the city app</li>
                </ul>
            </div>

            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">MasterCare — Patient Mobile App (iOS &amp; Android)</p>
                <ul>
                    <li>Patients browse their own medical history as a timeline, get <strong>AI-generated health summaries with citations</strong> back to source records</li>
                    <li>Receive medication and follow-up reminders</li>
                </ul>
            </div>
        </div>
    `,

    other: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">AI Pharmacist Assistant - Major Vietnamese Pharmacy Retail Chain</p>
                <p><i>AI / ML Architect - Proof of Concept</i> | 2026</p>
            </div>

            <div class="block">
                <ul style="margin-top: 1.5rem;">
                    <li>POC for an in-store AI assistant supporting pharmacists across a <strong>1,000+ store retail chain</strong>: contextual customer engagement (Customer 360), cross-sell / up-sell, smart FEFO alerts, and omni-knowledge helpdesk (drug info, SOPs, HR)</li>
                    <li>Designed a multi-agent architecture (Intent Router, Context Manager, specialized agent swarms) delivered as a POS-integrated mini-app with A/B testing for safe rollout</li>
                </ul>
            </div>
        </div>
    `,

    sendo: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Sen Do Technology JSC - E-commerce Platform</p>
                <p><i>Data Scientist</i> | 07/2019 - 05/2022</p>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1.5rem;">Brand Detection</p>
                <ul>
                    <li>Developed <strong>Computer Vision AI models</strong> to extract brands from product images</li>
                    <li>Implemented <strong>Faster R-CNN, ResNet, and OCR models</strong> to detect and classify brands into 500 categories</li>
                    <li>Achieved <strong>over 90% accuracy</strong>, improving market management efficiency by <strong>300%</strong></li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Sendo Search Engine Optimization</p>
                <ul>
                    <li>Led efforts to enhance the Sendo search engine, designing ranking logic and optimizing product visibility</li>
                    <li>Result: <strong>CTR improved from 38% to 47%</strong></li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Search Query Category Mapping</p>
                <ul>
                    <li>Developed a <strong>deep learning model</strong> to categorize search queries, improving product relevance</li>
                    <li>Achieved <strong>97% precision and 80% recall</strong>, increasing overall search CTR by <strong>1%</strong></li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Search Query Auto-Correction</p>
                <ul>
                    <li>Implemented a <strong>misspelling correction model</strong> that refines user queries before processing in Elasticsearch</li>
                    <li>Based on research paper: <i>Using the Web for Language-Independent Spellchecking and Autocorrection (Google)</i></li>
                    <li>Improved query accuracy by <strong>60%</strong> from test datasets</li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Search Query Auto-Filtering</p>
                <ul>
                    <li>Developed a <strong>sequence labeling model (CRF)</strong> to extract product attributes (price, size, color, location) from queries</li>
                    <li>Automatically applies relevant filters to refine search results</li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Synonym Dictionary for Elasticsearch</p>
                <ul>
                    <li>Built a <strong>dictionary of 2,000+ synonym pairs</strong> to improve query interpretation</li>
                    <li>Trained a <strong>Word2Vec skip-gram model</strong> on 19 million product descriptions</li>
                    <li>Extracted <strong>highly similar words</strong> to enhance Elasticsearch search accuracy</li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Product Title Scoring System</p>
                <ul>
                    <li>Developed a <strong>scoring model</strong> to rank product titles based on relevance and quality</li>
                    <li>Implemented <strong>two distinct models</strong>:</li>
                    <li style="padding-left: 1.5rem;"><strong>Title Spamming Score</strong>: Detects and penalizes spam-like product titles</li>
                    <li style="padding-left: 1.5rem;"><strong>Title Completeness Score</strong>: Rewards well-structured, informative titles</li>
                    <li>Titles flagged as spam are <strong>excluded from top search results</strong>, improving user experience</li>
                </ul>
            </div>
        </div>
    `,
    
    fpt: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">FPT Software</p>
                <p><i>Machine Learning Engineer</i> | 07/2018 - 07/2019</p>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1.5rem;">OCR-Based Vehicle Registration Recognition</p>
                <ul>
                    <li>Developed an OCR-based model for vehicle registration recognition, achieving <strong>90% accuracy</strong></li>
                    <li>Improved document processing efficiency through automated extraction of license plate details</li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Anomaly Detection in Automotive Sensor Data</p>
                <ul>
                    <li>Implemented an anomaly detection system to identify irregularities in automotive sensor data</li>
                    <li>Enhanced predictive maintenance by detecting potential failures before they occur</li>
                </ul>
            </div>
        </div>
    `,
    
    education: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Master of Artificial Intelligence</p>
                <p>RMIT University | 2024 - 2026 (Graduated)</p>
                <p><i>Grade: Distinction | Scholarship Awarded</i></p>
                <p style="margin-top: 0.5rem;">Focus on advanced ML, deep learning, and AI systems.</p>
                <p style="margin-top: 0.5rem;"><strong>Best Project Award</strong> – AI Postgraduate Project: <i>"GuideFlow: An Explainable, LLM-Constructed Clinical Decision Support System for Diabetes Management"</i> (industry partner: AstraZeneca).</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464; margin-top: 2rem;">Bachelor of Engineering</p>
                <p>Vaasa University of Applied Sciences | 2014 - 2018</p>
                <p><i>Software Engineering</i></p>
                <p style="margin-top: 0.5rem;">International degree; strong foundation in software and algorithms.</p>
            </div>
        </div>
    `,
    
    skills: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">LLM &amp; AI Agents</p>
                <p>LangGraph, LangChain, LlamaIndex, multi-agent systems, MCP (Model Context Protocol), tool calling, OpenAI / Anthropic (Claude) APIs</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">RAG &amp; Vector Search</p>
                <p>RAG pipelines, embeddings, hybrid &amp; semantic search, grounded answers with citations; pgvector, Qdrant, Milvus, Elasticsearch</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">LLM Evaluation &amp; Observability</p>
                <p>DeepEval, Langfuse, LLM-as-a-judge, RAG &amp; agent evaluation</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Machine Learning &amp; Deep Learning</p>
                <p>PyTorch, TensorFlow / Keras, scikit-learn, LightGBM, XGBoost, CatBoost; Time Series, NLP, Recommender Systems, Computer Vision</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">MLOps &amp; Deployment</p>
                <p>MLflow, ONNX, A/B testing &amp; Multi-Armed Bandit, Docker, Kubernetes, CI/CD, FastAPI, Grafana</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Programming</p>
                <p>Python, SQL</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Big Data Technologies</p>
                <p>Apache Spark, Kafka, Hadoop, Airflow, GCP, BigQuery, Pub/Sub</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Databases &amp; Search</p>
                <p>PostgreSQL, MongoDB, Redis, Elasticsearch</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Languages</p>
                <p>English (fluent), Vietnamese (native)</p>
            </div>
        </div>
    `,
    
    volunteer: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Nhu Chua He Co Cuoc Chia Ly – People Reunification Portal</p>
                <p><i>Volunteer Data Scientist / AI Engineer</i></p>
            </div>
            <div class="block">
                <p style="margin-top: 1rem;">Developed a GenAI-powered matching system to support locating missing persons and reconnecting separated families.</p>
            </div>
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Key contributions</p>
                <ul>
                    <li>Designed AI workflows leveraging <strong>NLP and semantic search</strong> to analyze incomplete, noisy, and unstructured user-submitted information</li>
                    <li>Collaborated with FPT Cloud to deploy and operate production systems at scale</li>
                    <li>Successfully launched public platforms: <a href="https://nhuchuahecocuocchialy.com" target="_blank" style="color: #83a6ff;">nhuchuahecocuocchialy.com</a> and <a href="https://portal.nhuchuahecocuocchialy.com" target="_blank" style="color: #83a6ff;">portal.nhuchuahecocuocchialy.com</a></li>
                    <li>Built a secure user portal for case submission, authentication, and AI-assisted candidate suggestion</li>
                </ul>
            </div>
        </div>
    `,
    
    awards: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Certifications and Awards</p>
            </div>
            <div class="block">
                <ul>
                    <li><strong>Best Project Award – RMIT AI Postgraduate Project</strong> - GuideFlow, AstraZeneca partner (2026)</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><strong>Excellent Project Award – Dispatch Engine</strong> (2025)</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><strong>The Contributor Award</strong> - Be Group (2024)</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><strong>Top Performer of The Year</strong> - Data Scientist at Be Group (2023)</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><strong>Top Performer of The Year</strong> - Data Scientist at Be Group (2022)</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><strong>Best Employee Of Organic Growth Tribe</strong> - Data Scientist at Sendo (2021)</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><strong>Best Employee Of The Year Award</strong> - Data Scientist at Sendo (2020)</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><strong>Data Science Mentor</strong> at MASSP - Math and Science Summer Program (2021)</li>
                </ul>
            </div>
        </div>
    `,
    
    contact: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Let's Connect</p>
                <p>Email: <a href="mailto:phucthanhvuong@gmail.com" style="color: #83a6ff;">phucthanhvuong@gmail.com</a></p>
                <p>Phone: <a href="tel:+84966097061" style="color: #83a6ff;">(+84) 966097061</a></p>
                <p>Location: Ho Chi Minh City, Vietnam</p>
            </div>
            <div class="block">
                <p style="margin-top: 1.5rem;">GitHub: <a href="https://github.com/thanhvuong1605" target="_blank" style="color: #83a6ff;">github.com/thanhvuong1605</a></p>
                <p>LinkedIn: <a href="https://linkedin.com/in/thanh-vuong-182449b0" target="_blank" style="color: #83a6ff;">linkedin.com/in/thanh-vuong-182449b0</a></p>
            </div>
            <div class="block">
                <p style="margin-top: 1rem;">Open to collaboration and new opportunities in ML/AI and data science.</p>
            </div>
        </div>
    `,
    
    cv: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Download CV</p>
                <p>Get the latest version of my resume:</p>
            </div>
            <div class="block">
                <p style="margin-top: 1.5rem;">
                    <a href="ThanhVuong_CV_202610.pdf" download style="color: #83a6ff; font-size: 1.1rem;">
                        📄 Download CV (PDF)
                    </a>
                </p>
                <p style="margin-top: 1rem; color: var(--text-tertiary);">Last updated: August 2026</p>
            </div>
        </div>
    `,
    
    resume: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Download CV</p>
                <p>Get the latest version of my resume:</p>
            </div>
            <div class="block">
                <p style="margin-top: 1.5rem;">
                    <a href="ThanhVuong_CV_202610.pdf" download style="color: #83a6ff; font-size: 1.1rem;">
                        📄 Download CV (PDF)
                    </a>
                </p>
                <p style="margin-top: 1rem; color: var(--text-tertiary);">Last updated: August 2026</p>
            </div>
        </div>
    `,
    
    ls: `
        <div class="nav-links">
            <a href="#" data-command="about">about</a>
            <a href="#" data-command="experience">experience</a>
            <a href="#" data-command="education">education</a>
            <a href="#" data-command="skills">skills</a>
            <a href="#" data-command="awards">awards</a>
            <a href="#" data-command="volunteer">volunteer</a>
            <a href="#" data-command="cv">cv</a>
            <a href="#" data-command="contact">contact</a>
        </div>
    `,
    
    help: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Available commands:</p>
                <ul>
                    <li><span style="color: var(--accent-color);">about</span> - Learn about Thanh Vuong</li>
                    <li><span style="color: var(--accent-color);">experience</span> - View work experience (then type: masterhive, be, sendo, fpt, volunteer, or other)</li>
                    <li><span style="color: var(--accent-color);">education</span> - Academic background</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><span style="color: var(--accent-color);">skills</span> - Technical skills</li>
                    <li><span style="color: var(--accent-color);">awards</span> - Certifications and awards</li>
                    <li><span style="color: var(--accent-color);">volunteer</span> - Volunteer project (People Reunification Portal)</li>
                    <li><span style="color: var(--accent-color);">cv</span> - Download CV/Resume</li>
                    <li><span style="color: var(--accent-color);">contact</span> - Contact information</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><span style="color: var(--accent-color);">ls</span> - List all commands</li>
                    <li><span style="color: var(--accent-color);">clear</span> - Clear the terminal</li>
                    <li><span style="color: var(--accent-color);">help</span> - Show this help message</li>
                </ul>
            </div>
        </div>
    `
};

let currentInput = '';
const inputText = document.getElementById('inputText');
const terminalOutput = document.getElementById('output');
const cursor = document.getElementById('cursor');
let isTypingAnimation = false;
let userCanType = false;

// Smooth block-by-block reveal
async function revealContent(container, htmlString) {
    isTypingAnimation = true;
    
    // Parse HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlString;
    
    // Create output container
    const outputDiv = document.createElement('div');
    container.appendChild(outputDiv);
    
    // Get all blocks (wrapped in .block class)
    const blocks = tempDiv.querySelectorAll('.block');
    
    if (blocks.length > 0) {
        // Process blocks
        for (const block of blocks) {
            const blockClone = document.createElement('div');
            blockClone.style.opacity = '0';
            blockClone.style.transform = 'translateY(20px)';
            
            // Copy all content from block
            blockClone.innerHTML = block.innerHTML;
            outputDiv.appendChild(blockClone);
            
            // Add click handlers for any links
            blockClone.querySelectorAll('a[data-command]').forEach(link => {
                link.addEventListener('click', handleLinkClick);
            });
            
            // Animate in smoothly
            await new Promise(resolve => setTimeout(resolve, 50));
            blockClone.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
            blockClone.style.opacity = '1';
            blockClone.style.transform = 'translateY(0)';
            
            // Wait before showing next block (smoother)
            await new Promise(resolve => setTimeout(resolve, 250));
            
            // Scroll smoothly
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        }
    } else {
        // Fallback for non-blocked content (like nav-links)
        const children = Array.from(tempDiv.children);
        for (const child of children) {
            const clone = child.cloneNode(true);
            clone.style.opacity = '0';
            clone.style.transform = 'translateY(20px)';
            outputDiv.appendChild(clone);
            
            // Add click handlers
            clone.querySelectorAll('a[data-command]').forEach(link => {
                link.addEventListener('click', handleLinkClick);
            });
            
            await new Promise(resolve => setTimeout(resolve, 40));
            clone.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
            clone.style.opacity = '1';
            clone.style.transform = 'translateY(0)';
            
            await new Promise(resolve => setTimeout(resolve, 180));
        }
    }
    
    isTypingAnimation = false;
}

// Link click handler with typing animation
async function handleLinkClick(e) {
    e.preventDefault();
    e.stopPropagation();
    
    if (!userCanType || isTypingAnimation) return;
    
    const command = e.currentTarget.getAttribute('data-command');
    if (!command) return;
    
    isTypingAnimation = true;
    
    // Type out the command
    currentInput = '';
    inputText.textContent = '';
    
    for (let i = 0; i < command.length; i++) {
        currentInput += command[i];
        inputText.textContent = currentInput;
        await new Promise(resolve => setTimeout(resolve, 60));
    }
    
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Execute the command
    executeCommand(command);
    currentInput = '';
    inputText.textContent = '';
    
    isTypingAnimation = false;
}

// Typing animation for page load
async function typeText(element, text, speed = 30) {
    isTypingAnimation = true;
    element.innerHTML = '';
    element.style.opacity = '1';
    
    for (let i = 0; i < text.length; i++) {
        if (text[i] === '\n') {
            element.innerHTML += '<br>';
        } else {
            element.innerHTML += text[i];
        }
        await new Promise(resolve => setTimeout(resolve, speed));
    }
    
    isTypingAnimation = false;
}

// Initial page load animation
async function initTypingAnimation() {
    const headline = document.querySelector('.headline');
    const promptLine = document.querySelector('.prompt-line');
    const navLinks = document.querySelectorAll('.nav-links a');
    const inputLine = document.querySelector('.input-line');
    
    // Initial pause - smoother start
    await new Promise(resolve => setTimeout(resolve, 500));
    
    headline.classList.remove('hidden');
    // Slower headline typing for better readability
    await typeText(headline, 'Thanh Vuong\nData Scientist / ML Engineer.', 50);
    
    // Longer pause after headline
    await new Promise(resolve => setTimeout(resolve, 400));
    
    // Smoother prompt line appearance
    promptLine.style.transition = 'opacity 0.3s ease-out';
    promptLine.classList.remove('hidden');
    
    // Pause before nav links
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Slower nav links appearance
    for (const link of navLinks) {
        link.style.transition = 'opacity 0.2s ease-out';
        link.classList.remove('hidden');
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    // AI hint after nav links
    const aiHint = document.querySelector('.ai-hint');
    if (aiHint) {
        await new Promise(resolve => setTimeout(resolve, 300));
        aiHint.style.transition = 'opacity 0.4s ease-out';
        aiHint.classList.remove('hidden');
    }

    // Show input line last with smoother transition
    await new Promise(resolve => setTimeout(resolve, 400));
    inputLine.style.transition = 'opacity 0.4s ease-out';
    inputLine.classList.remove('hidden');

    userCanType = true;
}

// Prevent text selection
document.addEventListener('selectstart', (e) => {
    if (e.target.tagName !== 'A' && !e.target.closest('.command-output')) {
        e.preventDefault();
    }
});

// Hidden input captures real text including IME composition (Vietnamese/Japanese/etc.)
const hiddenInput = document.createElement('input');
hiddenInput.type = 'text';
hiddenInput.id = 'hiddenInput';
hiddenInput.setAttribute('autocomplete', 'off');
hiddenInput.setAttribute('autocorrect', 'off');
hiddenInput.setAttribute('autocapitalize', 'off');
hiddenInput.setAttribute('spellcheck', 'false');
hiddenInput.style.cssText = 'position:fixed;left:-9999px;top:0;width:1px;height:1px;opacity:0;border:0;padding:0;';
document.body.appendChild(hiddenInput);

const focusHidden = () => {
    if (userCanType && !isTypingAnimation) hiddenInput.focus();
};

hiddenInput.addEventListener('input', () => {
    if (isTypingAnimation || !userCanType) {
        hiddenInput.value = currentInput;
        return;
    }
    currentInput = hiddenInput.value;
    inputText.textContent = currentInput;
});

hiddenInput.addEventListener('blur', () => setTimeout(focusHidden, 10));

// Focus handling
document.addEventListener('click', (e) => {
    if (e.target.tagName !== 'A' && userCanType && !isTypingAnimation) {
        focusHidden();
    }
});

// Keyboard input — only special keys; printable chars handled by hidden input
document.addEventListener('keydown', (e) => {
    if (isTypingAnimation || !userCanType) {
        if (e.key !== 'Tab') e.preventDefault();
        return;
    }

    if (e.target.tagName === 'A') return;

    if (e.key === 'Enter') {
        e.preventDefault();
        executeCommand(currentInput.trim());
        currentInput = '';
        hiddenInput.value = '';
        inputText.textContent = '';
    } else if (e.key === 'Tab') {
        e.preventDefault();
        const possibleCommands = Object.keys(commands).filter(cmd =>
            cmd.startsWith(currentInput.toLowerCase())
        );
        if (possibleCommands.length === 1) {
            currentInput = possibleCommands[0];
            hiddenInput.value = currentInput;
            inputText.textContent = currentInput;
        }
    } else if (e.key === 'l' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        clearTerminal();
        currentInput = '';
        hiddenInput.value = '';
        inputText.textContent = '';
    } else if (e.key === 'c' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        currentInput = '';
        hiddenInput.value = '';
        inputText.textContent = '';
    }
});

window.addEventListener('load', () => setTimeout(focusHidden, 100));

// Execute command
async function executeCommand(cmd) {
    if (!cmd) return;

    // Add command to history
    const commandLine = document.createElement('div');
    commandLine.className = 'prompt-line command-history';
    commandLine.innerHTML = `
        <span class="prompt-path">/dev/thanh-vuong</span>
        <span class="prompt-symbol">&gt;</span>
        <span class="user-command">${escapeHtml(cmd)}</span>
    `;
    terminalOutput.appendChild(commandLine);

    // Execute command
    if (cmd === 'clear') {
        clearTerminal();
        chatHistory = [];
        return;
    }

    const cmdLower = cmd.toLowerCase();
    if (commands[cmdLower]) {
        await revealContent(terminalOutput, commands[cmdLower]);
    } else {
        await askAI(cmd);
    }
}

let chatHistory = [];
const MAX_HISTORY = 20;

async function askAI(question) {
    const thinking = document.createElement('div');
    thinking.className = 'command-output';
    thinking.innerHTML = `<div class="block"><p class="ai-thinking" style="color: var(--accent-color);">thinking<span class="ai-dots">...</span></p></div>`;
    terminalOutput.appendChild(thinking);
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });

    let dots = 0;
    const dotsEl = thinking.querySelector('.ai-dots');
    const dotsInterval = setInterval(() => {
        dots = (dots + 1) % 4;
        if (dotsEl) dotsEl.textContent = '.'.repeat(dots);
    }, 400);

    try {
        const res = await fetch('/api/ask/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, history: chatHistory.slice(-MAX_HISTORY) })
        });

        if (res.status === 429) {
            clearInterval(dotsInterval);
            thinking.remove();
            await revealContent(terminalOutput, `<div class="command-output"><div class="block"><p class="error-output">Rate limited. Please slow down and try again in a minute.</p></div></div>`);
            return;
        }
        if (!res.ok || !res.body) {
            // Stream endpoint unavailable — fall back to the JSON endpoint
            clearInterval(dotsInterval);
            thinking.remove();
            await askAIJson(question);
            return;
        }

        clearInterval(dotsInterval);
        thinking.remove();

        // Render tokens as they stream in, terminal-style
        const wrap = document.createElement('div');
        wrap.className = 'command-output';
        wrap.innerHTML = `<div class="block"><p style="color: var(--accent-color); margin-bottom: 8px;">[ai]</p><p class="ai-answer"></p></div>`;
        terminalOutput.appendChild(wrap);
        const answerEl = wrap.querySelector('.ai-answer');

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let raw = '';
        const render = () => {
            answerEl.innerHTML = raw.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>');
        };
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            raw += decoder.decode(value, { stream: true });
            render();
            window.scrollTo({ top: document.body.scrollHeight });
        }
        raw += decoder.decode();
        render();
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });

        chatHistory.push({ role: 'user', content: question });
        chatHistory.push({ role: 'assistant', content: raw });
        if (chatHistory.length > MAX_HISTORY) chatHistory = chatHistory.slice(-MAX_HISTORY);
    } catch (e) {
        clearInterval(dotsInterval);
        thinking.remove();
        await revealContent(terminalOutput, `<div class="command-output"><div class="block"><p class="error-output">Network error. Type 'help' for available commands.</p></div></div>`);
    }
}

// Non-streaming fallback (old /api/ask JSON endpoint)
async function askAIJson(question) {
    try {
        const res = await fetch('/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, history: chatHistory.slice(-MAX_HISTORY) })
        });
        if (!res.ok) {
            await revealContent(terminalOutput, `<div class="command-output"><div class="block"><p class="error-output">AI unavailable (${res.status}). Type 'help' for available commands.</p></div></div>`);
            return;
        }
        const data = await res.json();
        const rawAnswer = data.answer || '';
        chatHistory.push({ role: 'user', content: question });
        chatHistory.push({ role: 'assistant', content: rawAnswer });
        if (chatHistory.length > MAX_HISTORY) chatHistory = chatHistory.slice(-MAX_HISTORY);

        const answer = rawAnswer.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>');
        const html = `<div class="command-output"><div class="block"><p style="color: var(--accent-color); margin-bottom: 8px;">[ai]</p><p>${answer}</p></div></div>`;
        await revealContent(terminalOutput, html);
    } catch (e) {
        await revealContent(terminalOutput, `<div class="command-output"><div class="block"><p class="error-output">Network error. Type 'help' for available commands.</p></div></div>`);
    }
}

// Clear terminal
function clearTerminal() {
    terminalOutput.innerHTML = `
        <h1 class="headline">Thanh Vuong<br>Data Scientist / ML Engineer.</h1>
        
        <div class="prompt-line">
            <span class="prompt-path">/dev/thanh-vuong</span>
            <span class="prompt-symbol">&gt;</span>
            <span class="prompt-command">ls</span>
        </div>
        
        <div class="nav-links">
            <a href="#" data-command="about">about</a>
            <a href="#" data-command="experience">experience</a>
            <a href="#" data-command="education">education</a>
            <a href="#" data-command="skills">skills</a>
            <a href="#" data-command="awards">awards</a>
            <a href="#" data-command="volunteer">volunteer</a>
            <a href="#" data-command="cv">cv</a>
            <a href="#" data-command="contact">contact</a>
        </div>

        <p class="ai-hint">tip: this terminal is AI-powered — just type any question, e.g. "how did Thanh double revenue with ML?"</p>
    `;

    addLinkHandlers();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Add click handlers to all command links
function addLinkHandlers() {
    document.querySelectorAll('a[data-command]').forEach(link => {
        link.addEventListener('click', handleLinkClick);
    });
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize
window.addEventListener('load', async () => {
    document.body.setAttribute('tabindex', '-1');
    await initTypingAnimation();
    addLinkHandlers();
    document.body.focus();
});
