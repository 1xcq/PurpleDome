import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		eel: window.eel
	}
});

export default app;