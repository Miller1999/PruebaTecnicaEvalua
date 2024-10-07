<template>
	<div v-if="isVisible" class="modal d-block" tabindex="-1">
		<div class="modal-dialog modal-dialog-centered">
			<div class="modal-content">
				<header class="modal-header">
					<h3 class="modal-title">{{ title }}</h3>
					<button type="button" class="btn-close" @click="closeModal"></button>
				</header>
				<div class="modal-body">
					<slot></slot>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "ProductCreate",
	props: {
		title: {
			type: String,
			required: true,
		},
		isVisible: {
			type: Boolean,
			default: false,
		},
		isEditing: {
			type: Boolean,
			default: false,
		},
	},
	methods: {
		closeModal() {
			this.$emit("close");
			this.$emit("closeEdit");
		},
	},
};
</script>

<style lang="scss" scoped>
@import "../../stylessheets/helpers/variables";
.modal {
	background-color: rgba(0, 0, 0, 0.5);
}
.modal-content {
	border-radius: 0.25rem;
}
</style>
