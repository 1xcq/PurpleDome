<script>
	import { onMount } from 'svelte';
	import { runningChallenge, selectedChallenge, challenges, machineSignal } from './lib/stores'

	/** svelte components **/
	import Challenge from './components/Challenge.svelte'
    import Sidebar from './components/Sidebar.svelte';
    import Loading from './components/Loading.svelte';
	
	/** props **/
	export let eel;

	// point eel websocket to python instance
	eel.set_host('ws://localhost:8080')

	onMount(async () => {
		const cs = await fetchChallenges();
		challenges.set(cs);
	});

	async function fetchChallenges() {
		let c = await eel.list_challenges()();
		return c;
	}

	function updateRunning(index) {
		runningChallenge.set(index);
    	const value = $machineSignal;
    	machineSignal.update(() => value);
	}
	window.eel.expose(updateRunning, "update_running");
	// WARN: must use window.eel to keep parse-able eel.expose{...}
</script>

<main class="flex w-full h-full py-4 text-white">
	<Sidebar eel={eel}></Sidebar>
	
	<div class="p-8 w-full overflow-auto">
	{#if $selectedChallenge === ""}
		<h2 class="font-bold text-3xl">WELCOME!</h2>
		<p class="mt-16 text-lg">
			First up a few additional infos: 
			<br>
			<br>
			Creating machines for the first time may take a while as vagrant has to download, update and boot the boxes. 
			<strong class="text-bold">Please be patient!</strong>
			<br>
			<br>
			If all packages were correctly installed machines should be accessible through the shown network or their hostnames.
			(Example > target1.local)
			<br>
			<br>
			Purple Dome reuses target machines. Because of it we can only run one challenge at once. Starting another challenge will shutdown the running challenge.
			<br>
			<br>
			All flags follow the format: <strong class="text-bold">flag&#123; &#125;</strong>
			<br>
			<br>
			In the top right corner are hints (?) that may help if you are stuck on a challenge.
		</p>
	{:else}
		{#key $selectedChallenge}
			<Challenge eel={eel} selectedChallenge={$selectedChallenge}/>
		{/key}
	{/if}
	</div>
</main>

