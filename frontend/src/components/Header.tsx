import { Link } from '@tanstack/react-router'

export default function Header() {
  return (
    <header className="p-2 flex gap-2 bg-black text-white justify-between shadow-2xl shadow-white/10">
      <nav className="flex flex-row">

        <div className="px-2 font-bold">
          <Link to="/">
            <img src="@/public/logo512.png" alt="KowAI" className="w-10 h-10" />
          </Link>
        </div>

        <div className="px-2 font-bold">
          <Link to="/">Home</Link>
        </div>

        <div className="px-2 font-bold">
          <Link to="/features">Features</Link>
        </div>

        <div className="px-2 font-bold">
          <Link to="/pricing">Pricing</Link>
        </div>

        <div className="px-2 font-bold">
          <Link to="/blog">Blog</Link>
        </div>

        <div className="px-2 font-bold">
          <Link to="/about">About</Link>
        </div>
      </nav>
    </header>
  )
}
