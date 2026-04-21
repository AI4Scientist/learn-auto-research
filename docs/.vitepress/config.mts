/// <reference types="node" />
import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

const docsBase = "/learn-auto-research/";
const brandLogo = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23B8593E" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/><path d="M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/></svg>';
const githubRepoTreeLink = "https://github.com/AI4Scientist/learn-auto-research";

const zhLectureItems = [
  { text: "欢迎", link: "/zh/" },
  { text: "为什么手动迭代会失败", link: "/zh/lectures/lecture-01-why-manual-iteration-fails/" },
  { text: "什么是可测量的研究目标", link: "/zh/lectures/lecture-02-what-is-a-measurable-research-goal/" },
  { text: "5阶段循环的内部机制", link: "/zh/lectures/lecture-03-five-stage-loop-internals/" },
  { text: "被卡住时怎么办", link: "/zh/lectures/lecture-04-what-to-do-when-stuck/" },
  { text: "科学方法调试", link: "/zh/lectures/lecture-05-scientific-debugging/" },
  { text: "错误归零流水线", link: "/zh/lectures/lecture-06-error-crushing-pipeline/" },
  { text: "5专家视角预判", link: "/zh/lectures/lecture-07-five-expert-predict/" },
  { text: "对抗性精炼", link: "/zh/lectures/lecture-08-adversarial-refinement/" },
  { text: "STRIDE+OWASP自动安全审计", link: "/zh/lectures/lecture-09-stride-owasp-security/" },
  { text: "12维场景探索", link: "/zh/lectures/lecture-10-twelve-dimension-scenarios/" },
  { text: "通用发布流水线", link: "/zh/lectures/lecture-11-universal-ship-pipeline/" },
  { text: "过夜运行与高级模式", link: "/zh/lectures/lecture-12-overnight-runs-advanced/" }
];

const zhProjectItems = [
  { text: "欢迎", link: "/zh/projects/" },
  { text: "你的第一个研究循环", link: "/zh/projects/project-01-first-research-loop/" },
  { text: "从基线到最优", link: "/zh/projects/project-02-baseline-to-optimal/" },
  { text: "调试一个真实的故障系统", link: "/zh/projects/project-03-debug-real-failure/" },
  { text: "架构决策的自动化辩论", link: "/zh/projects/project-04-architecture-debate/" },
  { text: "完整的安全审计流水线", link: "/zh/projects/project-05-security-audit-pipeline/" },
  { text: "端到端自动化研究项目", link: "/zh/projects/project-06-end-to-end-research/" }
];

const zhResourceItems = [
  { text: "资料库总览", link: "/zh/resources/" },
  { text: "模板", link: "/zh/resources/templates/" },
  { text: "参考手册", link: "/zh/resources/reference/" },
  { text: "领域案例集", link: "/zh/resources/domain-examples/" }
];

const enLectureItems = [
  { text: "Welcome", link: "/en/" },
  { text: "Why Manual Iteration Fails", link: "/en/lectures/lecture-01-why-manual-iteration-fails/" },
  { text: "What Is a Measurable Research Goal", link: "/en/lectures/lecture-02-what-is-a-measurable-research-goal/" },
  { text: "Five-Stage Loop Internals", link: "/en/lectures/lecture-03-five-stage-loop-internals/" },
  { text: "What to Do When Stuck", link: "/en/lectures/lecture-04-what-to-do-when-stuck/" },
  { text: "Scientific Debugging", link: "/en/lectures/lecture-05-scientific-debugging/" },
  { text: "Error-Crushing Pipeline", link: "/en/lectures/lecture-06-error-crushing-pipeline/" },
  { text: "Five-Expert Prediction", link: "/en/lectures/lecture-07-five-expert-predict/" },
  { text: "Adversarial Refinement", link: "/en/lectures/lecture-08-adversarial-refinement/" },
  { text: "STRIDE+OWASP Security Audit", link: "/en/lectures/lecture-09-stride-owasp-security/" },
  { text: "12-Dimension Scenario Exploration", link: "/en/lectures/lecture-10-twelve-dimension-scenarios/" },
  { text: "Universal Ship Pipeline", link: "/en/lectures/lecture-11-universal-ship-pipeline/" },
  { text: "Overnight Runs & Advanced Patterns", link: "/en/lectures/lecture-12-overnight-runs-advanced/" }
];

const enProjectItems = [
  { text: "Welcome", link: "/en/projects/" },
  { text: "Your First Research Loop", link: "/en/projects/project-01-first-research-loop/" },
  { text: "Baseline to Optimal", link: "/en/projects/project-02-baseline-to-optimal/" },
  { text: "Debug a Real Failure", link: "/en/projects/project-03-debug-real-failure/" },
  { text: "Architecture Decision Debate", link: "/en/projects/project-04-architecture-debate/" },
  { text: "Security Audit Pipeline", link: "/en/projects/project-05-security-audit-pipeline/" },
  { text: "End-to-End Research Project", link: "/en/projects/project-06-end-to-end-research/" }
];

const enResourceItems = [
  { text: "Overview", link: "/en/resources/" },
  { text: "Templates", link: "/en/resources/templates/" },
  { text: "Reference", link: "/en/resources/reference/" },
  { text: "Domain Examples", link: "/en/resources/domain-examples/" }
];

export default withMermaid(
  defineConfig({
    base: docsBase,
    title: "Learn AutoResearch",
    description:
      "基于项目的自动化研究课程，使用 Karpathy 启发的自主改进循环。定义指标，设定目标，让 Agent 彻夜迭代。",
    cleanUrls: true,
    srcExclude: ["temp/**"],
    ignoreDeadLinks: true,
    head: [
      ['link', { rel: 'icon', type: 'image/svg+xml', href: brandLogo }]
    ],
    themeConfig: {
      logo: brandLogo,
      search: { provider: "local" },
      socialLinks: [{ icon: "github", link: githubRepoTreeLink }]
    },
    markdown: {
      theme: {
        light: 'github-light',
        dark: 'github-dark'
      }
    },
    mermaid: {
      theme: 'base',
      themeVariables: {
        primaryColor: '#F5EDE8',
        primaryBorderColor: '#D89380',
        primaryTextColor: '#252523',
        lineColor: '#C4735A',
        fontFamily: 'system-ui, sans-serif',
        fontSize: '18px'
      },
      flowchart: {
        nodeSpacing: 40,
        rankSpacing: 56,
        padding: 12
      }
    },
    locales: {
      root: {
        label: "简体中文",
        lang: "zh-CN",
        link: "/zh/",
        themeConfig: {
          nav: [
            { text: "讲义", link: zhLectureItems[1].link, activeMatch: '^/zh/(lectures/.*)?$' },
            { text: "项目", link: zhProjectItems[0].link, activeMatch: '^/zh/projects/' },
            { text: "资料库", link: "/zh/resources/", activeMatch: '^/zh/resources/' },
            { text: "Try AutoResearch", link: "https://github.com/karpathy/autoresearch", target: "_blank", rel: "noopener noreferrer" }
          ],
          sidebar: {
            '/zh/projects/': [{ text: "项目", items: zhProjectItems }],
            '/zh/resources/': [{ text: "资料库", items: zhResourceItems }],
            '/zh/': [{ text: "讲义", items: zhLectureItems }]
          },
          outline: { level: [2, 3] },
          docFooter: { prev: "上一篇", next: "下一篇" },
          lastUpdated: { text: "最后更新于" },
          returnToTopLabel: "回到顶部",
          sidebarMenuLabel: "菜单",
          darkModeSwitchLabel: "主题",
          lightModeSwitchTitle: "切换到浅色模式",
          darkModeSwitchTitle: "切换到深色模式",
          socialLinks: [{ icon: "github", link: githubRepoTreeLink }]
        }
      },
      en: {
        label: "English",
        lang: "en",
        link: "/en/",
        themeConfig: {
          nav: [
            { text: "Lectures", link: enLectureItems[1].link, activeMatch: '^/en/(lectures/.*)?$' },
            { text: "Projects", link: enProjectItems[0].link, activeMatch: '^/en/projects/' },
            { text: "Library", link: "/en/resources/", activeMatch: '^/en/resources/' },
            { text: "Try AutoResearch", link: "https://github.com/karpathy/autoresearch", target: "_blank", rel: "noopener noreferrer" }
          ],
          sidebar: {
            '/en/projects/': [{ text: "Projects", items: enProjectItems }],
            '/en/resources/': [{ text: "Resource Library", items: enResourceItems }],
            '/en/': [{ text: "Lectures", items: enLectureItems }]
          },
          socialLinks: [{ icon: "github", link: githubRepoTreeLink }]
        }
      }
    }
  })
);
