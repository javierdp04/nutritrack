export const API_BASE = "http://localhost:5000/api";

export type ApiError = { error: string; code: string };

const TOKEN_KEY = "nt_token";
const ROL_KEY = "nt_rol";
const NOMBRE_KEY = "nt_nombre";

export const auth = {
	get token() { return localStorage.getItem(TOKEN_KEY); },
	get rol() { return localStorage.getItem(ROL_KEY); },
	get nombre() { return localStorage.getItem(NOMBRE_KEY); },
	get isAuthenticated() { return Boolean(localStorage.getItem(TOKEN_KEY)); },
	save(token: string, rol: string, nombre: string) {
		localStorage.setItem(TOKEN_KEY, token);
		localStorage.setItem(ROL_KEY, rol);
		localStorage.setItem(NOMBRE_KEY, nombre);
	},
	clear() {
		localStorage.removeItem(TOKEN_KEY);
		localStorage.removeItem(ROL_KEY);
		localStorage.removeItem(NOMBRE_KEY);
	},
};

export async function api<T = unknown>(
	path: string,
	options: RequestInit & { auth?: boolean } = {},
): Promise<T> {
	const headers = new Headers(options.headers);
	headers.set("Content-Type", "application/json");
	if (options.auth && auth.token) {
		headers.set("Authorization", `Bearer ${auth.token}`);
	}

	const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
	const text = await res.text();
	const body = text ? JSON.parse(text) : null;

	if (!res.ok) {
		if (res.status === 401 && options.auth) {
			auth.clear();
			window.location.href = "/login";
		}
		throw body as ApiError;
	}
	return body as T;
}

export function requireAuth() {
	if (!auth.isAuthenticated) {
		window.location.href = "/login";
	}
}

export function requireAdmin() {
	if (!auth.isAuthenticated) {
		window.location.href = "/login";
		return;
	}
	if (auth.rol !== "admin") {
		window.location.href = "/dashboard";
	}
}

export function logout() {
	auth.clear();
	window.location.href = "/login";
}
