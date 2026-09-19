export default function debugNavPage() {
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl font-bold mb-8">Debug Navigation Page</h1>
            <div className="flex flex-col gap-4">
                <a href="/hotels" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">Go to Hotels Page</a>
                <a href="/hotels/manage?role=Admin" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">Go to Hotels Manage Page</a>
                <a href="/ferry" className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition">Go to Ferry Page</a>
                <a href="/ferry/manage?role=Admin" className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition">Go to Ferry Manage Page</a>
                <a href="/theme-parks" className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 transition">Go to Theme Park Page</a>
                <a href="/theme-parks/manage?role=Admin" className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 transition">Go to Theme Manage Park Page</a>
            </div>
        </div>
    )
}