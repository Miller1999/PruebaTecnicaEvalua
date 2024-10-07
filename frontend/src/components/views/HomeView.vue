<template>
	<div class="container">
		<div class="nav">
			<div class="buttons d-flex justify-content-center mb-3">
				<button class="btn btn-primary">
					<span>{{ $t("inventory.filter") }}</span>
					<i class="bi bi-funnel"></i>
				</button>
				<button class="btn btn-success" @click="showModal = true">
					<span>{{ $t("inventory.add") }}</span>
					<i class="bi bi-plus-circle"></i>
				</button>
			</div>
		</div>
		<!-- large screens -->
		<table v-if="isLargeScreen" class="table table-center">
			<thead class="">
				<tr>
					<th scope="col">{{ $t("inventory.name") }}</th>
					<th scope="col">{{ $t("inventory.quantity") }}</th>
					<th scope="col">{{ $t("inventory.price") }}</th>
					<th scope="col">{{ $t("inventory.supplier") }}</th>
					<th scope="col">{{ $t("inventory.action") }}</th>
				</tr>
			</thead>
			<tbody>
				<tr scope="row" v-for="(product, index) in products" :key="index">
					<td>{{ product.name }}</td>
					<td>{{ product.quantity }}</td>
					<td>{{ Math.round(product.price_unit * 100) / 100 }}</td>
					<td>{{ product.supplier }}</td>
					<td class="table-buttons">
						<button
							class="btn btn-primary btn-sm"
							@click="editProduct(product.id_product)"
						>
							<i class="bi bi-pencil"></i>
						</button>
						<button
							class="btn btn-danger btn-sm"
							@click="deleteProduct(product.id_product)"
						>
							<i class="bi bi-trash"></i>
						</button>
					</td>
				</tr>
			</tbody>
		</table>
		<!-- small screens -->
		<section v-else class="row">
			<article v-for="(product, index) in products" :key="index" class="card">
				<div class="card-body"></div>
				<h5 class="card-title">
					{{ $t("inventory.name") }}: {{ product.name }}
				</h5>
				<p class="card-text">
					<strong>{{ $t("inventory.quantity") }}:</strong>
					{{ product.quantity }}
				</p>
				<p class="card-text">
					<span>{{ $t("inventory.price") }}:</span>
					{{ Math.round(product.price_unit * 100) / 100 }}
				</p>
				<p class="card-text">
					<span>{{ $t("inventory.supplier") }}:</span> {{ product.supplier }}
				</p>
				<div class="card__actions">
					<button
						class="btn btn-primary btn-sm"
						@click="editProduct(product.id_product)"
					>
						<i class="bi bi-pencil"></i>
					</button>
					<button
						class="btn btn-danger btn-sm"
						@click="deleteProduct(product.id_product)"
					>
						<i class="bi bi-trash"></i>
					</button>
				</div>
			</article>
		</section>
		<ProductCreate
			:isVisible="showModal"
			:isEditing="isEditing"
			:title="formTitle"
			@close="showModal = false"
			@closeEdit="isEditing = false"
			@save="saveProduct"
		>
			<form @submit.prevent="saveProduct">
				<div class="form-group">
					<label for="name">Nombre del producto</label>
					<p v-if="errors.name" class="error">{{ errors.name }}</p>
				</div>
				<input
					id="name"
					type="text"
					class="form-control"
					v-model="newProduct.name"
					placeholder="Nombre del producto"
					@input="clearError('name')"
				/>
				<div class="form-group">
					<label for="quantity">Cantidad</label>
					<p v-if="errors.quantity" class="error">{{ errors.quantity }}</p>
				</div>
				<input
					id="quantity"
					type="number"
					class="form-control"
					v-model="newProduct.quantity"
					placeholder="Cantidad"
					@input="clearError('quantity')"
				/>
				<div class="form-group">
					<label for="price">Precio</label>
					<p v-if="errors.price_unit" class="error">{{ errors.price_unit }}</p>
				</div>
				<input
					id="price"
					type="number"
					class="form-control"
					v-model="newProduct.price_unit"
					placeholder="Precio"
					@input="clearError('price_unit')"
				/>
				<div class="form-group">
					<label for="id_supplier">Proveedor</label>
					<p v-if="errors.id_supplier" class="error">
						{{ errors.id_supplier }}
					</p>
				</div>

				<select
					id="id_supplier"
					class="form-control"
					v-model="newProduct.id_supplier"
				>
					<option value="" disabled selected>Selecciona un proveedor</option>
					<option
						v-for="supplier in suppliers"
						:key="supplier.id_supplier"
						:value="supplier.id_supplier"
					>
						{{ supplier.name }}
					</option>
				</select>

				<button type="submit" class="btn btn-primary mt-3">Añadir</button>
			</form>
		</ProductCreate>
	</div>
</template>

<script>
import VAPI from "@/http_common";
import { HTTP_STATUS, SERVICE_NAMES } from "@/app_constants";
import ProductCreate from "./ProductCreate.vue";
export default {
	name: "HomeView",
	components: {
		ProductCreate,
	},
	data() {
		return {
			products: [],
			suppliers: [],
			isLargeScreen: true,
			isEditing: false,
			showModal: false,
			newProduct: {
				name: "",
				price_unit: null,
				id_supplier: null,
				quantity: null,
			},
			errors: {},
		};
	},
	mounted() {
		this.getAllSuppliers();
		this.getAllProducts();
		this.checkScreenSize();
		window.addEventListener("resize", this.checkScreenSize);
	},
	computed: {
		formTitle() {
			return this.isEditing
				? this.$t("inventory.edit")
				: this.$t("inventory.add");
		},
	},
	methods: {
		async getAllProducts() {
			try {
				let response = await VAPI.get(`${SERVICE_NAMES.INVENTORY}/get-all`);
				if (response.status == HTTP_STATUS.OK) {
					this.products = response.data;
				}
			} catch (error) {
				console.error(error);
			}
		},
		async saveProduct() {
			this.errors = {};
			if (!this.newProduct.name) {
				this.errors.name = "El nombre del producto es requerido";
			}
			if (!this.newProduct.quantity || this.newProduct.quantity <= 0) {
				this.errors.quantity = "La cantidad debe ser mayor a 0";
			}
			if (!this.newProduct.price_unit || this.newProduct.price_unit <= 0) {
				this.errors.price_unit = "El precio debe ser mayor a 0";
			}
			if (!this.newProduct.id_supplier) {
				this.errors.id_supplier = "El proveedor es requerido";
			}

			if (Object.keys(this.errors).length === 0) {
				try {
					let response;
					if (this.isEditing) {
						// Si estamos editando, llama al método PUT
						response = await VAPI.put(
							`${SERVICE_NAMES.INVENTORY}/${this.newProduct.id_product}`,
							this.newProduct
						);
					} else {
						// Si estamos creando, llama al método POST
						response = await VAPI.post(
							`${SERVICE_NAMES.INVENTORY}/`,
							this.newProduct
						);
					}
					if (
						response.status ==
						(this.isEditing ? HTTP_STATUS.OK : HTTP_STATUS.CREATED)
					) {
						this.showModal = false; // Cierra el modal
						this.newProduct = {
							name: "",
							price_unit: null,
							id_supplier: null,
							quantity: null,
						};
						this.isEditing = false; // Resetea el estado de edición
					}
				} catch (error) {
					console.error(error);
				}
			}
			await this.getAllProducts(); // Actualiza la lista de productos
		},

		async editProduct(idProduct) {
			this.showModal = true; // Abre el modal
			this.isEditing = true; // Marca como editando
			try {
				let response = await VAPI.get(
					`${SERVICE_NAMES.INVENTORY}/${idProduct}`
				);
				if (response.status == HTTP_STATUS.OK) {
					this.newProduct = {
						...response.data, // Rellena newProduct con los datos del producto
					};
				}
			} catch (error) {
				console.error(error);
			}
		},
		async deleteProduct(idProduct) {
			try {
				let response = await VAPI.delete(
					`${SERVICE_NAMES.INVENTORY}/${idProduct}`
				);
				if (response.status == HTTP_STATUS.NO_CONTENT) {
					await this.getAllProducts();
				}
			} catch (error) {
				console.error(error);
			}
			await this.getAllProducts();
		},
		async getAllSuppliers() {
			try {
				let response = await VAPI.get(
					`${SERVICE_NAMES.INVENTORY}/get-all-suppliers`
				);
				if (response.status == HTTP_STATUS.OK) {
					this.suppliers = response.data;
				}
			} catch (error) {
				console.error(error);
			}
		},
		checkScreenSize() {
			// Establece si la pantalla es grande o pequeña
			this.isLargeScreen = window.innerWidth > 767;
		},
		clearError(field) {
			if (this.errors[field]) {
				if (field === "quantity" || field === "price_unit") {
					if (this.newProduct[field] > 0) {
						delete this.errors[field];
					}
				} else if (this.newProduct[field]) {
					delete this.errors[field];
				}
			}
		},
	},
};
</script>

<style lang="scss" scoped>
@import "../../stylessheets/helpers/variables";
.container {
	margin-bottom: 7rem;
	@media (max-width: 767px) {
		margin-top: 100px;
	}
}

.row {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
}
.nav {
	justify-content: center;
}
.card {
	width: 90%;
	.card__actions {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
		margin: 1rem 0;
	}
}
.table-buttons {
	button:last-child {
		margin-left: 1rem;
	}
}
.error {
	color: red;
}
.buttons {
	position: fixed;
	z-index: 10;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 1rem;
	padding: 1rem;
	button {
		display: flex;
		justify-content: center;
		align-items: center;
		border-radius: 50%;
		width: 50px;
		height: 50px;
		border: 1px solid transparent;
		i {
			font-size: 1.5rem;
		}
	}
	span {
		display: none;
	}
	@media (min-width: 767px) {
		position: inherit;
		button {
			width: 200px;
			border-radius: 10px;
		}
		span {
			display: block;
		}
		i {
			display: none;
		}
	}
}
.form-group {
	margin-bottom: 1rem;
	text-align: left;
	label {
		font-weight: bold;
	}
}
input {
	margin-bottom: 1rem;
}
</style>
