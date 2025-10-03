// Terminal commands and their outputs
const commands = {
    about: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">About Me</p>
                <p>Senior Data Scientist and Machine Learning Engineer Lead with 6+ years of experience building real-time ML systems for ride-hailing, e-commerce, and fintech platforms.</p>
            </div>
            <div class="block">
                <p>Currently pursuing Master of Artificial Intelligence at RMIT University with scholarship.</p>
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
                    <a href="#" data-command="be">be</a>
                    <a href="#" data-command="tiki">tiki</a>
                    <a href="#" data-command="sendo">sendo</a>
                    <a href="#" data-command="fpt">fpt</a>
                </div>
            </div>
        </div>
    `,
    
    be: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Be Group JSC - Ride-hailing Application</p>
                <p><i>Senior Data Scientist/Machine Learning Engineer Lead</i> | 08/2022 - Present</p>
            </div>
            
            <div class="block">
                <p style="margin-top: 1.5rem;">Led a team of 4 ML engineers to design and maintain real-time ML models for pricing, dispatch, and recommendations, car pool and delivery systems. Developed and optimized production ML pipelines, improving scalability and efficiency.</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Key Projects:</p>
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
                <p style="color: var(--accent-color); margin-top: 1rem;">Multi-Dispatch Engine</p>
                <ul>
                    <li>Built a predictive model to score rider-driver pairings for optimal matching</li>
                    <li>Implemented a linear sum assignment algorithm to maximize overall rider-driver match scores</li>
                    <li>Increased <strong>completion rate (CR) by 10%</strong> and reduced <strong>average pickup distance by 30%</strong></li>
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
    
    tiki: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Tiki - E-commerce Platform</p>
                <p><i>Senior Data Scientist - Financial Product</i> | 05/2022 - 08/2022</p>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1.5rem;">Customer Segmentation</p>
                <ul>
                    <li>Expanded customer segmentation in the CDP to enhance targeting for insurance marketing campaigns</li>
                    <li>Developed segmentation models and analyzed cluster characteristics to derive actionable insights</li>
                    <li>Collaborated with the business team to refine customer targeting strategies and optimize marketing effectiveness</li>
                </ul>
            </div>
            
            <div class="block">
                <p style="color: var(--accent-color); margin-top: 1rem;">Propensity Model</p>
                <ul>
                    <li>Designed propensity models to predict customer likelihood of clicking or purchasing</li>
                    <li>Achieved <strong>90% precision and 70% recall</strong>, generating a high-confidence list of potential customers for Tiki's insurance products</li>
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
                <p>RMIT University | 2024 - Present</p>
                <p><i>Scholarship Awarded</i></p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464; margin-top: 2rem;">Bachelor of Engineering</p>
                <p>Vaasa University of Applied Sciences | 2014 - 2018</p>
                <p><i>Software Engineering</i></p>
            </div>
        </div>
    `,
    
    skills: `
        <div class="command-output">
            <div class="block">
                <p class="section-title" style="color: #e86464;">Programming</p>
                <p>Python, SQL</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Machine Learning</p>
                <p>Deep Learning, Time Series, NLP, Recommender Systems</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Big Data Technologies</p>
                <p>Apache Spark, Kafka, Hadoop, Airflow, GCP, BigQuery, PubSub</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">DevOps & Deployment</p>
                <p>Docker, Kubernetes, CI/CD Pipelines, FastAPI, Grafana</p>
            </div>
            
            <div class="block">
                <p class="section-title" style="color: #e86464;">Databases</p>
                <p>Elasticsearch, PostgreSQL, MongoDB, Redis</p>
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
                <p>Location: Hochiminh, Vietnam</p>
            </div>
            <div class="block">
                <p style="margin-top: 1.5rem;">GitHub: <a href="https://github.com/thanhvuong1605" target="_blank" style="color: #83a6ff;">github.com/thanhvuong1605</a></p>
                <p>LinkedIn: <a href="https://linkedin.com/in/thanh-vuong-182449b0" target="_blank" style="color: #83a6ff;">linkedin.com/in/thanh-vuong-182449b0</a></p>
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
                    <a href="CV_ThanhVuong_2025.pdf" download style="color: #83a6ff; font-size: 1.1rem;">
                        📄 Download CV (PDF)
                    </a>
                </p>
                <p style="margin-top: 1rem; color: var(--text-tertiary);">Last updated: 2025</p>
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
                    <a href="CV_ThanhVuong_2025.pdf" download style="color: #83a6ff; font-size: 1.1rem;">
                        📄 Download CV (PDF)
                    </a>
                </p>
                <p style="margin-top: 1rem; color: var(--text-tertiary);">Last updated: 2025</p>
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
                    <li><span style="color: var(--accent-color);">experience</span> - View work experience (then type: be, tiki, sendo, or fpt)</li>
                    <li><span style="color: var(--accent-color);">education</span> - Academic background</li>
                </ul>
            </div>
            <div class="block">
                <ul>
                    <li><span style="color: var(--accent-color);">skills</span> - Technical skills</li>
                    <li><span style="color: var(--accent-color);">awards</span> - Certifications and awards</li>
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

// Focus handling
document.addEventListener('click', (e) => {
    if (e.target.tagName !== 'A' && userCanType && !isTypingAnimation) {
        document.body.focus();
    }
});

// Keyboard input
document.addEventListener('keydown', (e) => {
    if (isTypingAnimation || !userCanType) {
        if (e.key !== 'Tab') {
            e.preventDefault();
        }
        return;
    }
    
    if (e.target.tagName === 'A') return;

    if (['Enter', 'Backspace', 'Tab'].includes(e.key)) {
        e.preventDefault();
    }

    if (e.key === 'Enter') {
        executeCommand(currentInput.trim());
        currentInput = '';
        inputText.textContent = '';
    } else if (e.key === 'Backspace') {
        currentInput = currentInput.slice(0, -1);
        inputText.textContent = currentInput;
    } else if (e.key === 'Tab') {
        const possibleCommands = Object.keys(commands).filter(cmd => 
            cmd.startsWith(currentInput.toLowerCase())
        );
        if (possibleCommands.length === 1) {
            currentInput = possibleCommands[0];
            inputText.textContent = currentInput;
        }
    } else if (e.key === 'l' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        clearTerminal();
        currentInput = '';
        inputText.textContent = '';
    } else if (e.key === 'c' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        currentInput = '';
        inputText.textContent = '';
    } else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        currentInput += e.key;
        inputText.textContent = currentInput;
    }
});

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
        return;
    }

    const cmdLower = cmd.toLowerCase();
    if (commands[cmdLower]) {
        await revealContent(terminalOutput, commands[cmdLower]);
    } else {
        const errorHTML = `<div class="command-output"><div class="block"><p class="error-output">Command not found: ${escapeHtml(cmd)}</p><p>Type 'help' for available commands.</p></div></div>`;
        await revealContent(terminalOutput, errorHTML);
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
            <a href="#" data-command="cv">cv</a>
            <a href="#" data-command="contact">contact</a>
        </div>
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
