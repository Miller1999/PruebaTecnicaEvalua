import Vue from "vue"; // Importa la biblioteca Vue
import VueRouter from "vue-router"; // Importa el módulo Vue Router

// Importa las vistas que se utilizarán en las rutas
const HomeView = () => import("../components/views/HomeView.vue");
const NotFound = () => import("../components/shared/NotFound.vue");

// Utiliza el plugin VueRouter en Vue
Vue.use(VueRouter);

// Define las rutas de la aplicación
const routes = [
	{
		path: "/", // Ruta principal
		name: "home", // Nombre de la ruta
		component: HomeView, // Componente asociado a la ruta
		meta: { title: "Home" }, // Metadatos, como el título de la página
	},
	{
		// Ruta para manejar todas las rutas no encontradas
		path: "/:catchAll(.*)", // Captura todas las rutas no definidas
		name: "NotFound", // Nombre de la ruta
		component: NotFound, // Componente asociado a la ruta
		meta: { title: "Not Found" }, // Metadatos, como el título de la página
	},
];

// Crea una nueva instancia de VueRouter
const router = new VueRouter({
	mode: "history", // Usa el modo de historia para URLs limpias
	base: process.env.BASE_URL, // Base URL definida en las variables de entorno
	routes, // Asigna las rutas definidas anteriormente
});

// Middleware para establecer el título del documento antes de cada navegación
router.beforeEach((to, from, next) => {
	document.title = to.meta.title; // Establece el título del documento
	next(); // Continúa con la navegación
});

// Exporta la instancia de VueRouter para usarla en la aplicación
export default router;
