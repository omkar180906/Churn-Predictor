"use client";

import React, { useEffect, useRef, useState, useMemo } from "react";
import {
    motion,
    AnimatePresence,
    useTransform,
    useReducedMotion,
    useMotionValue,
    useSpring,
    MotionValue,
} from "framer-motion";

// ============================================================================
// Data Contracts & Types
// ============================================================================

export interface CompanyChurnOverview {
    category: string;
    churnRate: string;
    predictedChurners: string;
    riskLevel: "LOW" | "MEDIUM" | "HIGH";
    monthlyRevenueAtRisk: string;
    keyFactors: string[];
    recommendedAction: string;
    modelConfidence: number;
}

export interface CompanyCardItem {
    id: string;
    title: string;
    src: string;
    tagline?: string;
    churnOverview: CompanyChurnOverview;
}

export interface PerspectiveTunnelHeroProps {
    headline?: string;
    companies?: CompanyCardItem[];
    onSelectCompany?: (company: CompanyCardItem) => void;
    className?: string;
    externalProgress?: MotionValue<number>;
}

// ============================================================================
// Default Static Data — 9 Target Companies with Churn Insights
// ============================================================================

export const DEFAULT_COMPANIES: CompanyCardItem[] = [
    {
        id: "netflix",
        title: "Netflix",
        tagline: "Subscription Video On Demand",
        src: "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "Entertainment Streaming",
            churnRate: "3.2%",
            predictedChurners: "8.4M Users / Quarter",
            riskLevel: "LOW",
            monthlyRevenueAtRisk: "$129.5M",
            keyFactors: [
                "Price tier adjustments & password-sharing friction",
                "Inactivity window exceeding 28 consecutive days",
                "Major series completion without backlog engagement",
            ],
            recommendedAction:
                "Trigger personalized binge-recommendation push notifications and offer an automated 6-month ad-tier discount before renewal.",
            modelConfidence: 89.4,
        },
    },
    {
        id: "spotify",
        title: "Spotify",
        tagline: "Digital Audio & Music Streaming",
        src: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "Audio Streaming",
            churnRate: "3.9%",
            predictedChurners: "2.3M Subscribers",
            riskLevel: "LOW",
            monthlyRevenueAtRisk: "$25.1M",
            keyFactors: [
                "Student promotion plan expiration",
                "Shift in podcast exclusivity availability",
                "Drop in weekly listening hours (< 4 hrs/wk)",
            ],
            recommendedAction:
                "Deliver tailored daily mix reminders and surface 3-month family plan upgrade incentives.",
            modelConfidence: 91.2,
        },
    },
    {
        id: "amazon-prime",
        title: "Amazon Prime",
        tagline: "E-Commerce & Digital Media",
        src: "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "E-Commerce & Media",
            churnRate: "6.8%",
            predictedChurners: "11.2M Members",
            riskLevel: "MEDIUM",
            monthlyRevenueAtRisk: "$168.0M",
            keyFactors: [
                "Reduced monthly order frequency",
                "Prime Video ad-free tier transition friction",
                "Regional competitor grocery delivery incentives",
            ],
            recommendedAction:
                "Highlight cumulative shipping & Prime day savings breakdown in account dashboard before annual bill date.",
            modelConfidence: 87.5,
        },
    },
    {
        id: "adobe",
        title: "Adobe",
        tagline: "Creative Cloud SaaS Platform",
        src: "https://images.unsplash.com/photo-1626785774573-4b799315345d?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "Creative Software SaaS",
            churnRate: "9.4%",
            predictedChurners: "1.8M Freelancers & SMBs",
            riskLevel: "MEDIUM",
            monthlyRevenueAtRisk: "$95.3M",
            keyFactors: [
                "Emergence of lightweight generative AI substitutes",
                "Annual contract renewal cancellation page visits",
                "Underutilized multi-app bundle licenses",
            ],
            recommendedAction:
                "Proactively offer single-app downgrade flexibility or 3-month pause option when cancellation intent is detected.",
            modelConfidence: 85.8,
        },
    },
    {
        id: "verizon",
        title: "Verizon",
        tagline: "Wireless & Telecommunications",
        src: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "Telecommunications",
            churnRate: "14.2% (Annual)",
            predictedChurners: "1.2M Postpaid Accounts",
            riskLevel: "HIGH",
            monthlyRevenueAtRisk: "$102.4M",
            keyFactors: [
                "Device payoff milestone reached (contract end)",
                "Aggressive BYOD trade-in promotions from rivals",
                "Repeated cellular network support tickets in fringe areas",
            ],
            recommendedAction:
                "Prioritize loyalty 5G flagship phone upgrade subsidy and dispatch VIP priority customer care.",
            modelConfidence: 84.7,
        },
    },
    {
        id: "disney",
        title: "Disney+",
        tagline: "Direct-to-Consumer Entertainment",
        src: "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "Entertainment Streaming",
            churnRate: "4.8%",
            predictedChurners: "5.1M Accounts",
            riskLevel: "MEDIUM",
            monthlyRevenueAtRisk: "$71.4M",
            keyFactors: [
                "Post-tentpole franchise season finale drop-off",
                "Household password sharing enforcement",
                "Standalone vs trio-bundle pricing resistance",
            ],
            recommendedAction:
                "Cross-promote bundled Disney+/Hulu/ESPN+ tier with 15% multi-service retention discount.",
            modelConfidence: 88.9,
        },
    },
    {
        id: "salesforce",
        title: "Salesforce",
        tagline: "Enterprise CRM & Cloud Solutions",
        src: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "Enterprise B2B SaaS",
            churnRate: "7.2%",
            predictedChurners: "12,400 Organizations",
            riskLevel: "MEDIUM",
            monthlyRevenueAtRisk: "$184.2M",
            keyFactors: [
                "Low seat utilization (< 45% daily logins per seat)",
                "Corporate IT software stack consolidation",
                "Executive sponsor turnover at client company",
            ],
            recommendedAction:
                "Schedule executive business review with Customer Success Architect and deploy free workflow automation training.",
            modelConfidence: 93.1,
        },
    },
    {
        id: "att",
        title: "AT&T",
        tagline: "Fiber Internet & Mobile Network",
        src: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "Telecom & Fiber Broadband",
            churnRate: "15.3% (Annual)",
            predictedChurners: "1.4M Subscribers",
            riskLevel: "HIGH",
            monthlyRevenueAtRisk: "$118.7M",
            keyFactors: [
                "Suburban fiber transition delays",
                "Billing fee escalation disputes",
                "Customer service resolution time > 48 hours",
            ],
            recommendedAction:
                "Issue automatic billing credit, guarantee 24/7 dedicated fiber support, and bundle free autopay discount.",
            modelConfidence: 83.5,
        },
    },
    {
        id: "zoom",
        title: "Zoom",
        tagline: "Unified Communications & Virtual Collaboration",
        src: "https://images.unsplash.com/photo-1588196749597-9ff075ee6b5b?w=800&auto=format&fit=crop&q=80",
        churnOverview: {
            category: "Video Collaboration SaaS",
            churnRate: "3.1% (Enterprise) / 12% (Pro)",
            predictedChurners: "840K Pro Accounts",
            riskLevel: "MEDIUM",
            monthlyRevenueAtRisk: "$38.6M",
            keyFactors: [
                "Enterprise migration toward bundled office suites",
                "Decline in remote-first company policies",
                "Single-host Pro plan cancellation after seasonal project",
            ],
            recommendedAction:
                "Deliver AI Companion feature onboarding and showcase Zoom Phone + Rooms integrated value propositions.",
            modelConfidence: 86.8,
        },
    },
];

// ============================================================
// Internal Geometry & Animation Helpers
// ============================================================

interface TunnelCardData {
    item: CompanyCardItem;
    angleCos: number;
    angleSin: number;
    radiusFactorX: number;
    radiusFactorY: number;
    rotationZ: number;
    index: number;
}

const SPRING_CONFIG = { stiffness: 60, damping: 25, mass: 0.5 };

interface StageDimensions {
    width: number;
    height: number;
    isMobile: boolean;
}

function useCameraParallax(enabled: boolean) {
    const rawX = useMotionValue(0);
    const rawY = useMotionValue(0);
    const x = useSpring(rawX, SPRING_CONFIG);
    const y = useSpring(rawY, SPRING_CONFIG);

    useEffect(() => {
        if (!enabled) return;
        const onMove = (e: PointerEvent) => {
            rawX.set((e.clientX / window.innerWidth - 0.5) * 2);
            rawY.set((e.clientY / window.innerHeight - 0.5) * 2);
        };
        window.addEventListener("pointermove", onMove, { passive: true });
        return () => window.removeEventListener("pointermove", onMove);
    }, [enabled, rawX, rawY]);

    return { x, y };
}

// ============================================================
// Single Tunnel Card Component
// ============================================================

interface TunnelCardProps {
    card: TunnelCardData;
    progress: MotionValue<number>;
    pointer: { x: MotionValue<number>; y: MotionValue<number> };
    total: number;
    stage: StageDimensions;
    onCardClick: (item: CompanyCardItem) => void;
}

function TunnelCard({ card, progress, pointer, total, stage, onCardClick }: TunnelCardProps) {
    const staggerSpan = 0.55;
    const start = (card.index / total) * (1 - staggerSpan);
    const end = start + staggerSpan;

    const localProgress = useTransform(progress, [start, end], [0, 1]);

    const farZ = stage.isMobile ? -1200 : -1750;
    const nearZ = stage.isMobile ? 360 : 520;
    const z = useTransform(localProgress, [0, 1], [farZ, nearZ]);

    const opacity = useTransform(localProgress, [0, 0.16, 0.85, 0.98], [0, 1, 1, 0]);

    const cardWidth = stage.isMobile
        ? Math.max(140, Math.min(200, stage.width * 0.42))
        : Math.max(200, Math.min(290, stage.width * 0.19));

    const baseX = card.angleCos * (stage.width * card.radiusFactorX);
    const baseY = card.angleSin * (stage.height * card.radiusFactorY);
    const panStrength = stage.isMobile ? 18 : 45;

    const transform = useTransform(
        [z, pointer.x, pointer.y],
        ([currZ, px, py]: number[]) => {
            const offsetX = baseX - px * panStrength;
            const offsetY = baseY - py * panStrength;
            return `translate3d(calc(-50% + ${offsetX}px), calc(-50% + ${offsetY}px), ${currZ}px) rotateZ(${card.rotationZ}deg)`;
        }
    );

    const riskBadgeClass = {
        LOW: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
        MEDIUM: "bg-amber-500/20 text-amber-300 border-amber-500/40",
        HIGH: "bg-rose-500/20 text-rose-300 border-rose-500/40",
    }[card.item.churnOverview.riskLevel];

    return (
        <motion.div
            style={{
                width: cardWidth,
                transform,
                opacity,
                zIndex: card.index + 1,
            }}
            onClick={() => onCardClick(card.item)}
            className="pointer-events-auto absolute left-1/2 top-1/2 aspect-[4/5] will-change-transform select-none cursor-pointer group"
        >
            <div className="relative h-full w-full overflow-hidden rounded-2xl bg-neutral-900/90 shadow-2xl shadow-black/80 ring-1 ring-white/15 transition-all duration-500 group-hover:scale-105 group-hover:ring-amber-400/80 group-hover:shadow-[0_0_35px_rgba(234,170,0,0.35)] backdrop-blur-md">
                {/* Background Image */}
                <img
                    src={card.item.src}
                    alt={card.item.title}
                    draggable={false}
                    className="h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-110 opacity-75 group-hover:opacity-95"
                />

                {/* Dark Vignette Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/40 to-transparent pointer-events-none" />

                {/* Card Top Pill: Risk Indicator */}
                <div className="absolute top-3 right-3 z-10">
                    <span
                        className={`text-[10px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${riskBadgeClass} backdrop-blur-md shadow-sm`}
                    >
                        {card.item.churnOverview.riskLevel} RISK
                    </span>
                </div>

                {/* Card Bottom Meta */}
                <div className="absolute inset-x-0 bottom-0 p-4 sm:p-5 flex flex-col justify-end">
                    <span className="text-[11px] font-mono uppercase tracking-wider text-amber-400 font-semibold mb-0.5">
                        {card.item.churnOverview.churnRate} Churn Est.
                    </span>
                    <h3 className="text-lg sm:text-xl font-bold tracking-tight text-white drop-shadow-md">
                        {card.item.title}
                    </h3>
                    <p className="text-xs text-neutral-400 line-clamp-1 mt-0.5">
                        {card.item.tagline || card.item.churnOverview.category}
                    </p>
                    <div className="mt-2.5 flex items-center justify-between text-[11px] text-neutral-300 font-mono border-t border-white/10 pt-2">
                        <span>Inspect Risk</span>
                        <span className="text-amber-400 group-hover:translate-x-1 transition-transform">
                            →
                        </span>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}

// ============================================================
// Interactive Modal: Churn Prediction Overview
// ============================================================

interface ChurnModalProps {
    company: CompanyCardItem | null;
    onClose: () => void;
}

function ChurnOverviewModal({ company, onClose }: ChurnModalProps) {
    if (!company) return null;

    const { churnOverview } = company;
    const isLow = churnOverview.riskLevel === "LOW";
    const isMedium = churnOverview.riskLevel === "MEDIUM";

    const badgeStyle = isLow
        ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
        : isMedium
        ? "bg-amber-500/10 text-amber-400 border-amber-500/30"
        : "bg-rose-500/10 text-rose-400 border-rose-500/30";

    const progressFill = isLow
        ? "bg-emerald-400"
        : isMedium
        ? "bg-amber-400"
        : "bg-rose-500";

    return (
        <AnimatePresence>
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 select-text">
                {/* Backdrop */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                    className="absolute inset-0 bg-black/80 backdrop-blur-md"
                />

                {/* Modal Container */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.92, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.92, y: 20 }}
                    transition={{ type: "spring", damping: 26, stiffness: 260 }}
                    className="relative w-full max-w-2xl overflow-hidden rounded-3xl bg-neutral-950/95 border border-white/15 text-white shadow-2xl shadow-amber-500/10 z-10 max-h-[90vh] flex flex-col"
                >
                    {/* Header Banner */}
                    <div className="relative px-6 pt-6 pb-4 border-b border-white/10 flex items-start justify-between bg-gradient-to-r from-neutral-900/60 to-neutral-950">
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <span className="text-xs font-mono text-neutral-400 uppercase tracking-widest">
                                    {churnOverview.category}
                                </span>
                                <span
                                    className={`text-[10px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${badgeStyle}`}
                                >
                                    {churnOverview.riskLevel} RISK
                                </span>
                            </div>
                            <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">
                                {company.title}
                            </h2>
                            <p className="text-xs text-neutral-400 mt-0.5">
                                AI Predictive Churn Analytics & Cohort Profiling
                            </p>
                        </div>

                        {/* Close button */}
                        <button
                            onClick={onClose}
                            className="rounded-full p-2 text-neutral-400 hover:text-white hover:bg-white/10 transition-colors"
                            aria-label="Close modal"
                        >
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    {/* Content Scroll Area */}
                    <div className="overflow-y-auto p-6 space-y-6">
                        {/* High-level Metric Stat Grid */}
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                            <div className="rounded-xl bg-neutral-900/70 border border-white/10 p-3.5 text-center">
                                <span className="text-[11px] font-mono text-neutral-400 uppercase tracking-wider block">
                                    Churn Rate
                                </span>
                                <span className="text-xl font-extrabold text-amber-400 mt-1 block">
                                    {churnOverview.churnRate}
                                </span>
                            </div>
                            <div className="rounded-xl bg-neutral-900/70 border border-white/10 p-3.5 text-center">
                                <span className="text-[11px] font-mono text-neutral-400 uppercase tracking-wider block">
                                    At-Risk Cohort
                                </span>
                                <span className="text-lg font-bold text-white mt-1 block">
                                    {churnOverview.predictedChurners}
                                </span>
                            </div>
                            <div className="rounded-xl bg-neutral-900/70 border border-white/10 p-3.5 text-center">
                                <span className="text-[11px] font-mono text-neutral-400 uppercase tracking-wider block">
                                    Revenue At Risk
                                </span>
                                <span className="text-lg font-bold text-rose-400 mt-1 block">
                                    {churnOverview.monthlyRevenueAtRisk}
                                </span>
                            </div>
                            <div className="rounded-xl bg-neutral-900/70 border border-white/10 p-3.5 text-center">
                                <span className="text-[11px] font-mono text-neutral-400 uppercase tracking-wider block">
                                    Model Confidence
                                </span>
                                <span className="text-lg font-bold text-emerald-400 mt-1 block">
                                    {churnOverview.modelConfidence}%
                                </span>
                            </div>
                        </div>

                        {/* Model Probability Gauge */}
                        <div className="rounded-2xl bg-neutral-900/50 border border-white/10 p-4">
                            <div className="flex justify-between items-center text-xs font-mono mb-2">
                                <span className="text-neutral-300">Posterior Churn Probability</span>
                                <span className="text-amber-400 font-bold">{churnOverview.churnRate}</span>
                            </div>
                            <div className="h-2.5 w-full bg-neutral-800 rounded-full overflow-hidden">
                                <div
                                    className={`h-full ${progressFill} transition-all duration-700`}
                                    style={{
                                        width: `${Math.min(
                                            100,
                                            Math.max(15, parseFloat(churnOverview.churnRate) * 5)
                                        )}%`,
                                    }}
                                />
                            </div>
                        </div>

                        {/* Key Churn Drivers */}
                        <div>
                            <h4 className="text-xs font-mono uppercase tracking-widest text-neutral-400 mb-3 flex items-center gap-2">
                                <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
                                Top Predictive Churn Indicators (Gini Importance)
                            </h4>
                            <ul className="space-y-2">
                                {churnOverview.keyFactors.map((factor, idx) => (
                                    <li
                                        key={idx}
                                        className="text-xs sm:text-sm text-neutral-300 bg-neutral-900/60 border border-white/5 rounded-xl px-3.5 py-2.5 flex items-start gap-2.5"
                                    >
                                        <span className="text-amber-400 font-mono font-bold">0{idx + 1}.</span>
                                        <span>{factor}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        {/* Context-Aware Recommended Action */}
                        <div className="rounded-2xl bg-gradient-to-r from-amber-500/10 via-neutral-900/70 to-neutral-900/50 border border-amber-500/30 p-4 sm:p-5">
                            <h4 className="text-xs font-mono uppercase tracking-widest text-amber-400 font-bold mb-1.5">
                                Automated Retention Recommendation
                            </h4>
                            <p className="text-xs sm:text-sm text-neutral-200 leading-relaxed">
                                {churnOverview.recommendedAction}
                            </p>
                        </div>
                    </div>

                    {/* Footer Actions */}
                    <div className="px-6 py-4 border-t border-white/10 bg-neutral-900/50 flex flex-col sm:flex-row items-center justify-between gap-3">
                        <span className="text-[11px] font-mono text-neutral-400">
                            * Predictions computed using Random Forest Ensemble classifier.
                        </span>
                        <button
                            onClick={onClose}
                            className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-neutral-950 font-bold text-xs uppercase tracking-wider transition-colors shadow-lg shadow-amber-400/20"
                        >
                            Done
                        </button>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
}

// ============================================================
// Main Export: PerspectiveTunnelHero
// ============================================================

export default function PerspectiveTunnelHero({
    headline = "WILL YOUR CUSTOMER CHURN",
    companies = DEFAULT_COMPANIES,
    onSelectCompany,
    className = "",
    externalProgress,
}: PerspectiveTunnelHeroProps) {
    const containerRef = useRef<HTMLDivElement>(null);
    const reduce = useReducedMotion();

    const [activeCompany, setActiveCompany] = useState<CompanyCardItem | null>(null);

    const [stage, setStage] = useState<StageDimensions>({
        width: 1440,
        height: 900,
        isMobile: false,
    });

    useEffect(() => {
        const updateDimensions = () => {
            setStage({
                width: window.innerWidth,
                height: window.innerHeight,
                isMobile: window.innerWidth < 768,
            });
        };

        updateDimensions();
        window.addEventListener("resize", updateDimensions);
        return () => window.removeEventListener("resize", updateDimensions);
    }, []);

    // Internal spring for standalone mode if external progress not provided
    const internalRaw = useMotionValue(0);
    const internalSmooth = useSpring(internalRaw, {
        stiffness: 80,
        damping: 30,
        restDelta: 0.0001,
    });

    // Use external progress if provided; otherwise internal
    const smoothProgress = externalProgress || internalSmooth;

    // --------------------------------------------------------
    // Mobile Touch Swipe + Desktop Wheel (Only in Standalone mode)
    // --------------------------------------------------------
    useEffect(() => {
        if (externalProgress) return; // In page scroll mode, native page scroll drives it!

        const el = containerRef.current;
        if (!el) return;

        const handleWheel = (e: WheelEvent) => {
            e.preventDefault();
            const current = internalRaw.get();
            const delta = e.deltaY * 0.0008;
            const next = Math.min(1, Math.max(0, current + delta));
            internalRaw.set(next);
        };

        let touchStartY = 0;
        const handleTouchStart = (e: TouchEvent) => {
            if (e.touches.length === 1) {
                touchStartY = e.touches[0].clientY;
            }
        };

        const handleTouchMove = (e: TouchEvent) => {
            if (e.touches.length === 1) {
                if (activeCompany) return;
                const currentY = e.touches[0].clientY;
                const deltaY = touchStartY - currentY;
                touchStartY = currentY;

                e.preventDefault();
                const current = internalRaw.get();
                const delta = deltaY * 0.0022;
                const next = Math.min(1, Math.max(0, current + delta));
                internalRaw.set(next);
            }
        };

        el.addEventListener("wheel", handleWheel, { passive: false });
        el.addEventListener("touchstart", handleTouchStart, { passive: true });
        el.addEventListener("touchmove", handleTouchMove, { passive: false });

        return () => {
            el.removeEventListener("wheel", handleWheel);
            el.removeEventListener("touchstart", handleTouchStart);
            el.removeEventListener("touchmove", handleTouchMove);
        };
    }, [externalProgress, internalRaw, activeCompany]);

    const pointer = useCameraParallax(!reduce);

    // Headline animations
    const titleScale = useTransform(smoothProgress, [0, 0.45, 0.8], [0.75, 1, 1.4]);
    const titleOpacity = useTransform(smoothProgress, [0, 0.08, 0.45, 0.7], [0.2, 1, 1, 0]);
    const promptOpacity = useTransform(smoothProgress, [0, 0.12], [1, 0]);

    // Forward breakthrough camera acceleration (zoom-in through tunnel center)
    const cameraZoom = useTransform(smoothProgress, [0, 0.65, 0.95], [1, 1, 2.2]);
    const tunnelFade = useTransform(smoothProgress, [0, 0.75, 0.96], [1, 1, 0]);

    // Expanding Warp Aperture Portal
    const portalScale = useTransform(smoothProgress, [0.65, 0.88, 1], [0.2, 3.5, 7]);
    const portalOpacity = useTransform(smoothProgress, [0.65, 0.8, 0.96], [0, 1, 0]);

    // Futuristic Breakthrough Status Label
    const portalTextOpacity = useTransform(smoothProgress, [0.72, 0.84, 0.94], [0, 1, 0]);
    const portalTextScale = useTransform(smoothProgress, [0.72, 0.84, 0.94], [0.85, 1, 1.15]);

    // Golden Angle tunnel card configuration
    const tunnelCards: TunnelCardData[] = useMemo(() => {
        return companies.map((item, i) => {
            const goldenAngle = i * 137.5 * (Math.PI / 180);
            const radiusFactorX = 0.28 + (i % 3) * 0.08;
            const radiusFactorY = 0.26 + (i % 2) * 0.09;

            return {
                item,
                angleCos: Math.cos(goldenAngle),
                angleSin: Math.sin(goldenAngle),
                radiusFactorX,
                radiusFactorY,
                rotationZ: (i % 2 === 0 ? 1 : -1) * (3 + (i % 5) * 2),
                index: i,
            };
        });
    }, [companies]);

    const handleCardClick = (item: CompanyCardItem) => {
        setActiveCompany(item);
        if (onSelectCompany) {
            onSelectCompany(item);
        }
    };

    return (
        <div
            ref={containerRef}
            className={`relative h-[100svh] w-screen overflow-hidden bg-neutral-950 text-white select-none flex items-center justify-center ${className}`}
            style={{
                perspective: stage.isMobile ? "900px" : "1250px",
                transformStyle: "preserve-3d",
                touchAction: activeCompany ? "auto" : externalProgress ? "auto" : "none",
            }}
        >
            {/* Immersive Futuristic Background Grid & Ambient Glows */}
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(#3A0F34_1.5px,transparent_1.5px)] [background-size:32px_32px] [mask-image:radial-gradient(ellipse_75%_75%_at_50%_50%,#000_60%,transparent_100%)] opacity-40" />
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(234,170,0,0.12)_0%,transparent_70%)]" />
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(58,15,52,0.35)_0%,transparent_80%)]" />

            {/* Depth Ring Guides */}
            <div className="pointer-events-none absolute h-[48vmin] w-[48vmin] rounded-full border border-amber-400/15 animate-pulse" />
            <div className="pointer-events-none absolute h-[76vmin] w-[76vmin] rounded-full border border-dashed border-white/10" />

            {/* Zooming Scene Container with Camera Acceleration */}
            <motion.div
                style={{
                    scale: cameraZoom,
                    opacity: tunnelFade,
                    transformStyle: "preserve-3d",
                }}
                className="absolute inset-0 flex items-center justify-center pointer-events-none"
            >
                {/* Central Anchor Typography: "WILL YOUR CUSTOMER CHURN" */}
                <motion.div
                    style={{ scale: titleScale, opacity: titleOpacity }}
                    className="pointer-events-none z-0 flex flex-col items-center text-center px-4 max-w-4xl"
                >
                    <h1 className="text-4xl sm:text-6xl md:text-8xl font-black tracking-tighter leading-[0.9] bg-gradient-to-b from-white via-neutral-100 to-neutral-500 bg-clip-text text-transparent drop-shadow-2xl">
                        {headline}
                    </h1>
                </motion.div>

                {/* 3D Z-Space Plane Container */}
                <div
                    className="absolute inset-0 pointer-events-none"
                    style={{ transformStyle: "preserve-3d" }}
                >
                    {tunnelCards.map((card, i) => (
                        <TunnelCard
                            key={card.item.id || i}
                            card={card}
                            progress={smoothProgress}
                            pointer={pointer}
                            total={tunnelCards.length}
                            stage={stage}
                            onCardClick={handleCardClick}
                        />
                    ))}
                </div>
            </motion.div>

            {/* Futuristic Warp Aperture Ring (Portal breakthrough effect) */}
            <motion.div
                style={{
                    scale: portalScale,
                    opacity: portalOpacity,
                }}
                className="pointer-events-none absolute h-[50vmin] w-[50vmin] rounded-full border-2 border-amber-400 bg-gradient-to-r from-amber-400/20 via-purple-900/30 to-amber-400/20 shadow-[0_0_80px_rgba(234,170,0,0.6)] blur-[1px] z-10"
            />

            {/* Breakthrough Telemetry HUD Banner */}
            <motion.div
                style={{
                    opacity: portalTextOpacity,
                    scale: portalTextScale,
                }}
                className="pointer-events-none absolute z-20 flex flex-col items-center gap-2 text-center px-6"
            >
                <div className="flex items-center gap-2 text-xs font-mono tracking-[0.4em] uppercase text-amber-400 font-bold">
                    <span className="h-2 w-2 rounded-full bg-amber-400 animate-ping" />
                    ENTERING CHURN PULSE ENGINE
                </div>
                <div className="h-0.5 w-32 bg-gradient-to-r from-transparent via-amber-400 to-transparent" />
            </motion.div>

            {/* Scroll / Swipe Exploration Prompt */}
            <motion.div
                style={{ opacity: promptOpacity }}
                className="pointer-events-none absolute bottom-8 z-20 flex flex-col items-center gap-2 text-xs font-mono uppercase tracking-[0.3em] text-neutral-400"
            >
                <span>{stage.isMobile ? "Swipe to Explore" : "Scroll to Explore"}</span>
                <div className="h-6 w-px bg-gradient-to-b from-amber-400 to-transparent" />
            </motion.div>

            {/* Interactive Churn Prediction Overview Dialog */}
            <ChurnOverviewModal
                company={activeCompany}
                onClose={() => setActiveCompany(null)}
            />
        </div>
    );
}
