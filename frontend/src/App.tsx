import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "./components/layout/Layout";
import { AuthProvider } from "./features/auth/AuthContext";
import { CatalogPage } from "./pages/CatalogPage";
import { CategoriesPage } from "./pages/CategoriesPage";
import { ComingSoonPage } from "./pages/ComingSoonPage";
import { LoginPage } from "./pages/LoginPage";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<CatalogPage />} />
            <Route path="/categories" element={<CategoriesPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/about" element={<ComingSoonPage title="О нас" />} />
            <Route
              path="/register"
              element={<ComingSoonPage title="Регистрация" />}
            />
            <Route
              path="*"
              element={<ComingSoonPage title="Страница не найдена" />}
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
