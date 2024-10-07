<template>
	<div>
		<button @click="toggleTheme">
			<i v-if="currentTheme === 'dark'" class="bi bi-sun-fill"></i>
			<i v-else-if="currentTheme === 'light'" class="bi bi-moon-fill"></i>
		</button>
	</div>
</template>

<script>
export default {
	data() {
		return {
			currentTheme: localStorage.getItem("theme") || "light", // Inicializa con el tema guardado
		};
	},
	methods: {
		toggleTheme() {
			const newTheme = this.currentTheme === "light" ? "dark" : "light"; // Determina el nuevo tema
			localStorage.setItem("theme", newTheme); // Guarda el nuevo tema en localStorage
			this.applyTheme(newTheme); // Aplica el nuevo tema
			this.currentTheme = newTheme; // Actualiza el estado del componente
		},
		applyTheme(theme) {
			document.body.classList.remove("theme-light", "theme-dark");
			document.body.classList.add(`theme-${theme}`);
		},
	},
	mounted() {
		const savedTheme = localStorage.getItem("theme") || "light";
		this.applyTheme(savedTheme); // Aplica el tema guardado
		this.currentTheme = savedTheme; // Asegúrate de que currentTheme esté actualizado
	},
};
</script>

<style scoped>
button {
	border: none;
	background-color: transparent;
	padding: 0;
	margin: 0;
	cursor: pointer;
	i {
		font-size: 2rem;
	}
}
</style>
