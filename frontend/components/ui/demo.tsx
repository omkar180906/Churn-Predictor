"use client";

import React, { useState } from "react";
import PerspectiveTunnelHero, {
    CompanyCardItem,
} from "@/components/ui/perspective-tunnel-hero";

export default function DemoOne() {
    const [selectedCompany, setSelectedCompany] = useState<string | null>(null);

    return (
        <main className="relative min-h-screen w-full bg-neutral-950 text-white overflow-hidden">
            {/* Perspective Tunnel Hero */}
            <PerspectiveTunnelHero
                headline="WILL YOUR CUSTOMER CHURN"
                onSelectCompany={(company: CompanyCardItem) => {
                    console.log("Selected company for churn inspection:", company.title);
                    setSelectedCompany(company.title);
                }}
            />

            {/* Notification Toast for Demonstration */}
            {selectedCompany && (
                <div className="fixed bottom-4 right-4 z-40 bg-neutral-900/90 border border-amber-400/30 text-amber-300 text-xs font-mono px-4 py-2.5 rounded-xl shadow-xl backdrop-blur-md">
                    Inspecting Churn Cohort: <span className="font-bold text-white">{selectedCompany}</span>
                </div>
            )}
        </main>
    );
}
