import { CardSpotlight } from "@/components/ui/card-spotlight";
import { createRoute, type RootRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { LoaderTwo } from "@/components/ui/loader";

interface Plan {
    title: string,
    price: number,
    description: string,
    benefits: string[],
    cta: string,
}

const plans: Plan[] = [
    {
        title: "Free Plan",
        price: 0,
        description: "Access to basic features with limited usage.",
        benefits: [
            "Basic Task Management",
            "Limited Integrations",
            "Email Support"
        ],
        cta: "Get Started for Free"
    },
    {
        title: "Pro Plan",
        price: 15,
        description: "",
        benefits: [
            "Advanced Task Management",
            "Priority Support",
            "Custom Integrations"
        ],
        cta: "Upgrade now"
    },
    {
        title: "Enterprise Plan",
        price: 30,
        description: "A perfect option for more enterprise functionalities.",
        benefits: [
            "All Pro Features",
            "Dedicated Account Manager",
            "Custom Solutions"
        ],
        cta: "Contact us"
    }
];

const Pricing = () => {
    return (
        <div className="bg-black text-white pixelify-sans-400 text-center p-4 flex flex-col items-center h-full w-full">
            <div >
                <h1 className="text-4xl">Pricing Plans</h1>
                <p className="text-3xl">Choose a plan that suits your needs.</p>
            </div>
            <CardSpotlight>
                <h2 className="text-xl pixelify-sans-500 z-20 relative">Free Plan</h2>
                <p className="z-20 relative">Access to basic features with limited usage.</p>
                <ul className="list-disc list-inside z-20 relative">
                    <li>Basic Task Management</li>
                    <li>Limited Integrations</li>
                    <li>Email Support</li>
                </ul>
                <button className="mt-4 px-6 py-2 bg-blue-500 text-white rounded z-20 relative">Get Started</button>
            </CardSpotlight>
        </div>
    )
}

export default (parentRoute: RootRoute) => createRoute({
    path: "/pricing",
    component: Pricing,
    getParentRoute: () => parentRoute,
})