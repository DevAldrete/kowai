import { createRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { LoaderTwo } from '@/components/ui/loader'

import type { RootRoute } from '@tanstack/react-router'

const Features = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['jokes'],
    queryFn: async () =>
      await fetch(
        'https://v2.jokeapi.dev/joke/Any?blacklistFlags=political&lang=en&type=single',
      ).then((res) => res.json()),
  })
  return (
    <>
      { isLoading ? <LoaderTwo/> : <p className="text-2xl text-black pixelify-sans-400">{data.joke}</p>}
    </>
  )
}

export default (parentRouter: RootRoute) => createRoute({
  component: Features,
  getParentRoute: () => parentRouter,
  path: '/features',
})