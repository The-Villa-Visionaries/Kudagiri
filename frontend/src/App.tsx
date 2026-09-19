import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HotelsPage from "./pages/HotelsPage"
import ThemeParksPage from './pages/ThemeParksPage'
import FerryPage from './pages/FerryPage'
import RedirectPage from './pages/RedirectPage'
import NotFoundPage from './pages/NotFoundPage'
import ThemeParksManagePage from './pages/ThemeParksManagePage'
import FerryManagePage from './pages/FerryManagePage'
import DebugNavPage from './pages/DebugNavPage'
import HotelsManagePage from './pages/HotelsManagePage'

export default function App() {
    return(
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<RedirectPage />} />

                <Route path="/hotel" element={<HotelsPage />} />
                <Route path="/hotels" element={<HotelsPage />} />
                <Route path="/room" element={<HotelsPage />} />
                <Route path="/rooms" element={<HotelsPage />} />
                <Route path="/hotels/manage" element={<HotelsManagePage />} />

                <Route path="/park" element={<ThemeParksPage />} />
                <Route path="/theme-park" element={<ThemeParksPage />} />
                <Route path="/theme-parks" element={<ThemeParksPage />} />
                <Route path="/theme-parks/manage" element={<ThemeParksManagePage />} />
                
                <Route path="/ferry" element={<FerryPage />} />
                <Route path="/train" element={<FerryPage />} />
                <Route path="/Speedboat" element={<FerryPage />} />
                <Route path="/ferry/manage" element={<FerryManagePage />} />

                <Route path="/login" element={<RedirectPage />} />
                <Route path="/register" element={<RedirectPage />} />
                <Route path="/topup" element={<RedirectPage />} />
                <Route path="/promotions" element={<RedirectPage />} />
                
                <Route path="/admin" element={<RedirectPage />} />

                <Route path="/debug" element={<DebugNavPage />} />

                <Route path="*" element={<NotFoundPage />} />
            </Routes>
        </BrowserRouter>
    )
}