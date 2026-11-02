# Original CPA IS-audit case: control testing and evidence (2 November 2026)

**Status:** Independently authored fictional practice; arithmetic checked internally, subject-expert review pending. Maps provisionally to June 2024 CA24 Auditing and Assurance and CA34S2 Advanced Auditing and Assurance, with CA16 ICT prerequisites. The revised 2027 KASNEB CPA syllabus is not yet mapped. This is **not** an ICPAK, Bafunde or KASNEB question or answer.

## Scenario

A fictional Kenyan distribution company runs an accounting application. During an audit scoping review, you obtain the following synthetic control-test results:

| Area | Population or sample | Exceptions observed |
|---|---:|---:|
| Privileged accounts | 96 active privileged accounts | 7 lack multifactor authentication |
| User-access reviews | 96 privileged accounts | 12 accounts show no timely recertification |
| Application changes | 50 sampled production changes | 8 lack documented pre-deployment approval |
| Scheduled backup jobs | 120 jobs over the selected review period | 9 failures; 6 of those failures have no documented successful rerun |
| Segregation of duties | All relevant roles reviewed | 3 users can both create a supplier and approve supplier payments |

The 7 MFA exceptions and 12 recertification exceptions may overlap; no overlap count is given. No population size for all production changes is provided. Control objectives, actual loss history and the completeness/reliability of source system reports have **not** been established.

## Questions

1. Calculate the observed exception rates for MFA, access recertification, sampled change approvals, failed backup jobs and unresolved backup failures.
2. Identify three high-priority risks and propose a preventive or detective control for each.
3. Describe one independent audit procedure for each risk, including the evidence needed.
4. Explain why a 16% sample exception rate is not necessarily the population exception rate and why the access-control exceptions must not be added together as distinct affected accounts.
5. Distinguish control-design assessment from operating-effectiveness testing.

## Model response (internal arithmetic checked; independent academic review pending)

1. MFA exceptions: **7/96 = 7.29%**. Privileged access reviews not timely: **12/96 = 12.50%**. Change approvals absent: **8/50 = 16.00%** of *sampled* changes. Backup job failures: **9/120 = 7.50%**. Unresolved failures: **6/9 = 66.67%** of failed jobs, or **6/120 = 5.00%** of all scheduled jobs. The 6 are a subset of the 9, not an additional 6 failures.
2. Privileged access without MFA risks unauthorised administrative activity; require enforced MFA and exception monitoring. Incompatible supplier-creation and payment-approval rights risk fictitious vendors and payments; enforce role separation or independent compensating approval. Unapproved production changes risk unauthorised logic changes and inaccurate accounting; require a tracked approval, testing and deployment workflow. Backup failures without verified recovery risk prolonged disruption and data loss; require alerts, rerun escalation and periodic restoration testing.
3. Obtain an independently generated privileged-user inventory and authentication policy; reconcile to identity-provider MFA settings and inspect approved exceptions. Extract the role/permission matrix and test whether the three conflicting users have exercised both functions, examining logs and compensating approvals. Independently reconcile change tickets to deployment logs for the 50 selected changes and verify dated approvals before deployment. Reconcile job scheduler logs to failure alerts and successful reruns; perform or observe a controlled restore test.
4. The 50 changes are a sample, not the whole change population; selection method, population completeness and sampling uncertainty are unknown. The 7 MFA exceptions and 12 recertification exceptions could concern the same accounts; without intersection data the unique affected-account count lies between **12 and 19**, not automatically 19.
5. Design testing asks whether a properly specified control could prevent or detect the risk if implemented. Operating-effectiveness testing evaluates whether it actually operated consistently over the period, with reliable evidence and appropriate sample selection.

**Limitations:** No conclusion on actual audit opinion, fraud occurrence, overall assurance or material weakness follows from these synthetic counts alone. Check the relevant current professional standards, engagement context and official syllabus before teaching as examinable content. No commercial rights to third-party video slides, questions, logos or transcripts are conveyed by this original case.
