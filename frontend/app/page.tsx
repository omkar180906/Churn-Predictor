"use client";

import React, { useState, useEffect } from "react";
import {
  motion,
  useMotionValue,
  useSpring,
  useTransform,
} from "framer-motion";
import PerspectiveTunnelHero, {
  CompanyCardItem,
  DEFAULT_COMPANIES,
} from "@/components/ui/perspective-tunnel-hero";
import MLDashboardSection from "@/components/ml-dashboard-section";

export default function Home() {
  const [selectedCompany, setSelectedCompany] = useState<CompanyCardItem | null>(null);
  const [isAtDashboard, setIsAtDashboard] = useState(false);
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);

  // High-Speed Virtual progress motion value:
  // 0.00 -> 0.60: Swift flight through the 9 Company 3D Perspective Slides
  // 0.58 -> 0.72: Accelerated Camera Warp & Aperture Breakthrough
  // 0.70 -> 1.00: Live Python/Streamlit ML Dashboard Full-Screen View
  const rawProgress = useMotionValue(0);

  // Snappy spring physics for instant, zero-lag trackpad, wheel, and touch response
  const smoothProgress = useSpring(rawProgress, {
    stiffness: 190,
    damping: 22,
    mass: 0.18,
    restDelta: 0.0005,
  });

  // 1. 3D Tunnel internal depth progress: maps 0.0 - 0.60 to full tunnel depth (fast travel)
  const tunnelProgress = useTransform(smoothProgress, [0, 0.60], [0, 1]);

  // 2. Breakthrough camera warp & tunnel fade out
  const tunnelOpacity = useTransform(smoothProgress, [0.58, 0.72], [1, 0]);
  const tunnelScale = useTransform(smoothProgress, [0.58, 0.72], [1, 2.2]);

  // 3. Top landing page brand bar: strictly fades out BEFORE dashboard appears (ZERO overlapping text!)
  const heroHeaderOpacity = useTransform(smoothProgress, [0.52, 0.66], [1, 0]);

  // 4. Slide Navigation HUD: fades out smoothly before portal warp
  const hudOpacity = useTransform(smoothProgress, [0.52, 0.66], [1, 0]);

  // 5. ML Dashboard fade-in and smooth scale: docks fast
  const dashboardOpacity = useTransform(smoothProgress, [0.68, 0.76], [0, 1]);
  const dashboardScale = useTransform(smoothProgress, [0.68, 0.76], [0.98, 1]);

  // Sync state for dashboard active lock & slide indicator
  useEffect(() => {
    const unsub = smoothProgress.on("change", (latest) => {
      setIsAtDashboard(latest >= 0.72);

      // Compute active company slide (0 to 8)
      const ratio = Math.min(1, Math.max(0, latest / 0.60));
      const idx = Math.min(
        DEFAULT_COMPANIES.length - 1,
        Math.floor(ratio * DEFAULT_COMPANIES.length)
      );
      setCurrentSlideIndex(idx);
    });
    return () => unsub();
  }, [smoothProgress]);

  // Direct High-Speed Wheel, Touch & Keyboard Controller
  useEffect(() => {
    // Fast Wheel / Trackpad listener
    const handleWheel = (e: WheelEvent) => {
      // If inspecting a company card modal or if inside dashboard, let normal events proceed
      if (selectedCompany || isAtDashboard) return;

      e.preventDefault();
      const current = rawProgress.get();
      // Fast, responsive sensitivity: travel through tunnel in 2-3 gentle wheel ticks
      const delta = e.deltaY * 0.0019;
      const next = Math.min(1, Math.max(0, current + delta));
      rawProgress.set(next);
    };

    // Fast Touch listener for mobile
    let touchStartY = 0;
    const handleTouchStart = (e: TouchEvent) => {
      if (e.touches.length === 1) {
        touchStartY = e.touches[0].clientY;
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (selectedCompany || isAtDashboard) return;
      if (e.touches.length === 1) {
        const currentY = e.touches[0].clientY;
        const deltaY = touchStartY - currentY;
        touchStartY = currentY;

        e.preventDefault();
        const current = rawProgress.get();
        // Snappy mobile swipe response
        const delta = deltaY * 0.0045;
        const next = Math.min(1, Math.max(0, current + delta));
        rawProgress.set(next);
      }
    };

    // Keyboard navigation (Arrow keys, Space, PageUp/Down, Home, End)
    const handleKeyDown = (e: KeyboardEvent) => {
      if (selectedCompany || isAtDashboard) return;

      if (e.key === "ArrowDown" || e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {
        e.preventDefault();
        const current = rawProgress.get();
        rawProgress.set(Math.min(1, current + 0.075));
      } else if (e.key === "ArrowUp" || e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault();
        const current = rawProgress.get();
        rawProgress.set(Math.max(0, current - 0.075));
      } else if (e.key === "End" || e.key === "Enter") {
        e.preventDefault();
        rawProgress.set(0.85); // Direct jump to ML dashboard
      } else if (e.key === "Home" || e.key === "Escape") {
        e.preventDefault();
        rawProgress.set(0); // Return to slide 1
      }
    };

    window.addEventListener("wheel", handleWheel, { passive: false });
    window.addEventListener("touchstart", handleTouchStart, { passive: true });
    window.addEventListener("touchmove", handleTouchMove, { passive: false });
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("wheel", handleWheel);
      window.removeEventListener("touchstart", handleTouchStart);
      window.removeEventListener("touchmove", handleTouchMove);
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [selectedCompany, isAtDashboard, rawProgress]);

  // Instant return to slide 1
  const handleReturnToTunnel = () => {
    rawProgress.set(0);
  };

  // Fast jump directly to a company slide
  const handleJumpToSlide = (index: number) => {
    const target = (index / (DEFAULT_COMPANIES.length - 1)) * 0.55;
    rawProgress.set(target);
  };

  // Instant warp straight into the ML dashboard
  const handleSkipToDashboard = () => {
    rawProgress.set(0.85);
  };

  const activeCompanyName = DEFAULT_COMPANIES[currentSlideIndex]?.title || "Overview";

  return (
    <main className="fixed inset-0 w-screen h-[100svh] overflow-hidden bg-neutral-950 text-white select-none">
      {/* 
        Clean Minimal Top Brand Bar
        Rendered ONLY during the 3D Tunnel phase with smooth fade-out to guarantee ZERO overlapping text!
      */}
      {!isAtDashboard && (
        <motion.header
          style={{ opacity: heroHeaderOpacity }}
          className="fixed top-0 inset-x-0 z-30 flex items-center justify-between px-6 py-4 bg-transparent pointer-events-none"
        >
          <div className="flex items-center gap-2.5 pointer-events-auto">
            <span className="flex h-2.5 w-2.5 rounded-full bg-amber-400 animate-pulse shadow-[0_0_8px_#f59e0b]" />
            <span className="text-xs sm:text-sm font-mono tracking-widest font-black uppercase text-white drop-shadow-md">
              CHURN PULSE <span className="text-amber-400">3D</span>
            </span>
          </div>

          <button
            onClick={handleSkipToDashboard}
            className="pointer-events-auto flex items-center gap-1.5 px-3 py-1 rounded-full bg-neutral-900/80 hover:bg-neutral-800 border border-white/10 text-neutral-300 hover:text-white text-xs font-mono transition-all backdrop-blur-md cursor-pointer hover:border-amber-400/40"
          >
            <span>Skip to Dashboard</span>
            <span className="text-amber-400 font-bold">→</span>
          </button>
        </motion.header>
      )}

      {/* 
        Layer 1: 3D Perspective Tunnel Hero
        In-place 3D perspective flight through company slides without vertical document scroll
      */}
      <motion.div
        style={{
          opacity: tunnelOpacity,
          scale: tunnelScale,
          pointerEvents: isAtDashboard ? "none" : "auto",
        }}
        className="absolute inset-0 z-10 w-full h-full"
      >
        <PerspectiveTunnelHero
          headline="WILL YOUR CUSTOMER CHURN"
          externalProgress={tunnelProgress}
          onSelectCompany={(company) => setSelectedCompany(company)}
          onCloseModal={() => setSelectedCompany(null)}
        />
      </motion.div>

      {/* 
        Slide Navigation HUD (Active during 3D Tunnel Phase)
        Shows current company slide index, interactive dots, and navigation shortcuts
      */}
      {!isAtDashboard && (
        <motion.div
          style={{ opacity: hudOpacity }}
          className="pointer-events-none fixed bottom-6 inset-x-0 z-30 flex items-center justify-between px-6 sm:px-10"
        >
          {/* Active Company Pill Indicator */}
          <div className="pointer-events-auto flex items-center gap-2 bg-neutral-900/80 border border-white/10 backdrop-blur-md px-3.5 py-1.5 rounded-full text-xs font-mono shadow-xl">
            <span className="text-amber-400 font-bold">
              0{currentSlideIndex + 1} / 0{DEFAULT_COMPANIES.length}
            </span>
            <span className="text-neutral-500">•</span>
            <span className="text-white font-semibold">{activeCompanyName}</span>
          </div>

          {/* Interactive Slide Dots */}
          <div className="pointer-events-auto hidden md:flex items-center gap-1.5 bg-neutral-900/80 border border-white/10 backdrop-blur-md px-3 py-1.5 rounded-full shadow-xl">
            {DEFAULT_COMPANIES.map((company, idx) => {
              const isActive = idx === currentSlideIndex;
              return (
                <button
                  key={company.id}
                  onClick={() => handleJumpToSlide(idx)}
                  className={`h-2 rounded-full transition-all duration-200 cursor-pointer ${
                    isActive
                      ? "w-6 bg-amber-400 shadow-[0_0_8px_#f59e0b]"
                      : "w-2 bg-white/20 hover:bg-white/50"
                  }`}
                  title={`Slide ${idx + 1}: ${company.title}`}
                />
              );
            })}
          </div>

          {/* Shortcut to Dashboard */}
          <div className="pointer-events-auto flex items-center gap-2">
            <button
              onClick={handleSkipToDashboard}
              className="px-3.5 py-1.5 rounded-full bg-amber-400 hover:bg-amber-300 text-neutral-950 font-bold text-xs font-mono transition-all shadow-lg shadow-amber-400/20 cursor-pointer"
            >
              ML Dashboard →
            </button>
          </div>
        </motion.div>
      )}

      {/* 
        Layer 2: Live Full-Screen Python/Streamlit Machine Learning Dashboard
        Seamlessly takes over the full viewport when the tunnel traversal reaches breakthrough
      */}
      <motion.div
        style={{
          opacity: dashboardOpacity,
          scale: dashboardScale,
          pointerEvents: isAtDashboard ? "auto" : "none",
        }}
        className="fixed inset-0 z-40 w-screen h-screen overflow-hidden"
      >
        <MLDashboardSection />
      </motion.div>
    </main>
  );
}
