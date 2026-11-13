"use client";

import React, { useState, useEffect, useRef } from "react";

interface MLDashboardSectionProps {
    onReturnToTop?: () => void;
    className?: string;
}

export default function MLDashboardSection({
    onReturnToTop,
    className = "",
}: MLDashboardSectionProps) {
    const [isLoading, setIsLoading] = useState(true);
    const [hasError, setHasError] = useState(false);
    const [iframeKey, setIframeKey] = useState(0);
    const containerRef = useRef<HTMLDivElement>(null);

    const STREAMLIT_URL =
        process.env.NEXT_PUBLIC_STREAMLIT_URL || "http://localhost:8501/?embed=true";

    useEffect(() => {
        const timer = setTimeout(() => {
            if (isLoading) {
                // Remove loader quickly so live dashboard paints instantly
                setIsLoading(false);
            }
        }, 1200);
        return () => clearTimeout(timer);
    }, [isLoading]);

    const handleReload = () => {
        setIsLoading(true);
        setHasError(false);
        setIframeKey((prev) => prev + 1);
    };

    const handleToggleFullscreen = () => {
        if (!document.fullscreenElement) {
            containerRef.current?.requestFullscreen().catch(() => {});
        } else {
            document.exitFullscreen().catch(() => {});
        }
    };

    return (
        <section
            ref={containerRef}
            id="ml-dashboard-section"
            className={`fixed inset-0 w-screen h-[100svh] bg-neutral-950 text-white flex flex-col justify-start items-stretch overflow-hidden ${className}`}
            style={{ width: "100vw", height: "100vh" }}
        >
            {/* Top Sleek Dashboard Control Bar - Single clean header */}
            <div className="w-full h-12 bg-neutral-900 border-b border-white/10 px-4 sm:px-6 flex items-center justify-between shrink-0 z-30 shadow-md">
                <div className="flex items-center gap-3">
                    <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_10px_#10b981]" />
                    <div className="flex items-center gap-2">
                        <span className="text-xs sm:text-sm font-mono font-extrabold tracking-wider uppercase text-white">
                            CHURN <span className="text-amber-400">PREDICTOR</span>
                        </span>
                        <span className="text-[11px] font-mono text-neutral-400 hidden md:inline border-l border-white/10 pl-2">
                            Random Forest Classifier • 100 Trees • Accuracy: 77.86%
                        </span>
                    </div>
                </div>

                <div className="flex items-center gap-2.5 text-xs font-mono">
                    <button
                        onClick={handleReload}
                        className="px-2.5 py-1 rounded-md bg-neutral-800 hover:bg-neutral-700 text-neutral-300 hover:text-white border border-white/10 transition-colors"
                        title="Reload Dashboard Frame"
                    >
                        ↻ Sync
                    </button>

                    <button
                        onClick={handleToggleFullscreen}
                        className="px-2.5 py-1 rounded-md bg-neutral-800 hover:bg-neutral-700 text-neutral-300 hover:text-white border border-white/10 transition-colors hidden sm:inline-block"
                        title="Toggle Fullscreen"
                    >
                        ⛶ Fullscreen
                    </button>
                </div>
            </div>

            {/* True 100% Full Screen Iframe Container */}
            <div
                className="relative w-full flex-1 bg-neutral-950 overflow-hidden"
                style={{ width: "100%", height: "calc(100vh - 48px)", minHeight: "calc(100vh - 48px)" }}
            >
                {/* Non-blocking top loading indicator: never creates a blank black screen! */}
                {isLoading && (
                    <div className="absolute top-0 inset-x-0 h-0.5 bg-gradient-to-r from-amber-400 via-emerald-400 to-amber-400 animate-pulse z-20 pointer-events-none" />
                )}

                {/* Error State */}
                {hasError && (
                    <div className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-neutral-950 p-6 text-center">
                        <div className="text-rose-400 text-2xl mb-2">⚠️</div>
                        <h3 className="text-base font-bold text-white mb-2 font-mono">
                            Connection to Streamlit Engine Interrupted
                        </h3>
                        <p className="text-xs text-neutral-400 max-w-md mb-4 font-mono">
                            The Python backend server at localhost:8501 might be restarting. Click below to reconnect.
                        </p>
                        <button
                            onClick={handleReload}
                            className="px-4 py-2 rounded-xl bg-amber-400 hover:bg-amber-300 text-neutral-950 font-bold text-xs font-mono uppercase tracking-wider transition-colors"
                        >
                            Retry Connection
                        </button>
                    </div>
                )}

                {/* Fullscreen Iframe: explicit 100% width and height */}
                <iframe
                    key={iframeKey}
                    src={STREAMLIT_URL}
                    title="Customer Churn Prediction Engine"
                    loading="eager"
                    onLoad={() => {
                        setIsLoading(false);
                        setHasError(false);
                    }}
                    onError={() => {
                        setIsLoading(false);
                        setHasError(true);
                    }}
                    className="w-full h-full border-0 block"
                    style={{
                        width: "100%",
                        height: "100%",
                        minHeight: "100%",
                        display: "block",
                    }}
                    allow="clipboard-read; clipboard-write;"
                />
            </div>
        </section>
    );
}
