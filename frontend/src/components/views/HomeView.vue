<template>
	<div class="home">
		<div class="nav">
			<div class="buttons">
				<button>
					<span>{{ $t("inventory.filter") }}</span>
					<ion-icon name="funnel-outline"></ion-icon>
				</button>
				<button @click="showModal = true">
					<span>{{ $t("inventory.add") }}</span>
					<ion-icon name="add-outline"></ion-icon>
				</button>
			</div>
		</div>
		<!-- large screens -->
		<table v-if="isLargeScreen" class="table">
			<thead>
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
					<td>
						<b-button @click="editProduct(product.id_product)">
							<ion-icon name="create-outline"></ion-icon>
						</b-button>
						<b-button
							@click="deleteProduct(product.id_product)"
							variant="secondary"
						>
							<ion-icon name="trash-outline"></ion-icon>
						</b-button>
					</td>
				</tr>
			</tbody>
		</table>
		<!-- small screens -->
		<section v-else class="card__container">
			<article v-for="(product, index) in products" :key="index" class="card">
				<h2>{{ $t("inventory.name") }}: {{ product.name }}</h2>
				<p>
					<span>{{ $t("inventory.quantity") }}:</span> {{ product.quantity }}
				</p>
				<p>
					<span>{{ $t("inventory.price") }}:</span> {{ product.price }}
				</p>
				<p>
					<span>{{ $t("inventory.supplier") }}:</span> {{ product.supplier }}
				</p>
				<div class="card__actions">
					<b-button
						@click="
							$router.push({
								name: 'product',
								params: { idProduct: product.id_product },
							})
						"
					>
						<ion-icon name="create-outline"></ion-icon>
					</b-button>
					<b-button @click="deleteProduct(product.id_product)">
						<ion-icon name="trash-outline"></ion-icon>
					</b-button>
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

				<select id="id_supplier" v-model="newProduct.id_supplier">
					<option value="" disabled selected>Selecciona un proveedor</option>
					<option
						v-for="supplier in suppliers"
						:key="supplier.id_supplier"
						:value="supplier.id_supplier"
					>
						{{ supplier.name }}
					</option>
				</select>

				<button type="submit">Añadir</button>
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
/* Large screens */
.home {
	display: flex;
	flex-direction: column;
	align-items: center;
}
table {
	width: 90%;
	max-width: 1200px;
	margin: 1rem 0;
	border-collapse: collapse;
	border-spacing: 0;
	font-size: 1rem;
	thead {
		th {
			text-align: center;
			padding: 0.5rem;
			background-color: $ColorBodyBg;
		}
	}
	tbody {
		tr {
			border-bottom: 1px solid #ddd;
			td {
				padding: 0.5rem;
				text-align: center;
			}
			td:first-child {
				min-width: 250px;
				max-width: 250px;
			}
			td:last-child {
				display: flex;
				gap: 1rem;
				justify-content: center;
				button {
					padding: 0;
					display: flex;
					justify-content: center;
					align-items: center;
					width: 50px;
					height: 50px;
					border: 1px solid transparent;
					background-color: transparent;
					ion-icon {
						font-size: 1.5rem;
						color: #000;
					}
				}
				button:last-child {
					ion-icon {
						color: red;
					}
				}
				button:hover {
					background-color: transparent;
					border: 1px solid gray;
				}
			}
		}
		tr:nth-child(even) {
			background-color: $ColorVueBg;
		}
	}
}

/* Small screens */
.card__container {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	width: 100%;
	margin: 1rem 0 3rem 0;
}
.card {
	min-width: 250px;
	max-width: 250px;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	padding: 1rem;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
	transition: all 0.3s ease;

	&:hover {
		box-shadow: 0 8px 16px rgba(0, 0, 0, 0.26);
	}
	h2 {
		font-size: 1rem;
		font-weight: 900;
	}
	p {
		span {
			font-weight: bold;
		}
	}
	.card__actions {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
		button {
			width: 50px;
			height: 50px;
			border: 1px solid transparent;
			background-color: transparent;
			ion-icon {
				font-size: 1.5rem;
				color: #000;
			}
		}
		button:last-child {
			ion-icon {
				color: red;
			}
		}
	}
}
.card:nth-child(even) {
	background-color: $ColorVueBg;
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
		background-color: var(--bs-blue);
		ion-icon {
			font-size: 1.5rem;
			color: #000;
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
		ion-icon {
			display: none;
		}
	}
}
</style>
