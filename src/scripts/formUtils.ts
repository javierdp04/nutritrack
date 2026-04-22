export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const setError = (field: string, message: string) => {
	const el = document.querySelector(`[data-error-for="${field}"]`);
	if (el) el.textContent = message;
	const input = document.getElementById(field);
	if (input) input.classList.toggle("invalid", Boolean(message));
};

export const clearErrors = (fields: string[]) =>
	fields.forEach(f => setError(f, ""));

export const setValue = (id: string, value: string | number) => {
				const el = document.getElementById(id) as HTMLInputElement | HTMLSelectElement | null;
				if (el) el.value = String(value);
			};
