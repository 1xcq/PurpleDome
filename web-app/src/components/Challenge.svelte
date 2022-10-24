<script>
    import { selectedChallenge, runningChallenge, challenges, machineSignal } from "../lib/stores"
    import Loading from "./Loading.svelte";
	export let eel;

	let machines = [];
    let isLoading = false
    let isStarting = false

	async function list() {
        isLoading = true
        machines = [];
		machines = await eel.list_challenge_machines($selectedChallenge)();
        isLoading = false
    }

    async function start() {
        isStarting = true
        const running = await eel.start_challenge($selectedChallenge)();
        runningChallenge.set(running);
        console.log(running)
        list();
        isStarting = false
        console.log("after return")
    }
    
    $: list(), $machineSignal;
    $: list(), $selectedChallenge;
</script>

<div class="flex flex-col gap-8 w-full">
    
    <h2 class="text-lg font-bold">
        TITLE: 
        <span class="font-normal">
            {$challenges[$selectedChallenge].name}
        </span>
    </h2>
    <h2 class="text-lg font-bold">
        DESCRIPTION:
        <p class="font-normal">
            {$challenges[$selectedChallenge].description}
        </p>
    </h2>

    <!-- MACHINES -->
    <ul class="flex flex-col justify-start gap-4 w-full p-4 card bg-slate-800">
        <h2 class="text-lg font-bold">MACHINES:</h2>
        {#if machines.length > 0}
            {#each machines as machine}
            <li>
                <span>- {machine.name}:</span> 
                <span class={machine.state === "RUNNING" ? "badge badge-accent" : "badge badge-ghost"}>{machine.state}</span>
            </li>
            {/each}
            <button disabled={isStarting} 
                class="btn btn-success w-48 disabled:bg-gray-800" 
                on:click={async () => await start()}>
                    {#if isStarting}
                        <Loading></Loading>Loading
                    {:else}
                        START MACHINES
                    {/if}
            </button>     
        {:else}
            <Loading>Loading ...</Loading>
        {/if}
    </ul>
</div>
