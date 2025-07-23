import { createRoute, type RootRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { LoaderTwo } from "@/components/ui/loader";

const About = () => {
    return (
        <div className="text-2xl text-black dark:text-white dark:bg-black pixelify-sans-400 text-center p-4 flex flex-col items-center">
            <h1>About KowAI</h1>
            <p>KowAI is your virtual assistant designed to enhance productivity and streamline your tasks.</p>
            <p>Learn more about our features and how we can help you achieve more.</p>
        </div>
    )
}

export default (parentRoute: RootRoute) => createRoute({
    component: About,
    getParentRoute: () => parentRoute,
    path: '/about',
})