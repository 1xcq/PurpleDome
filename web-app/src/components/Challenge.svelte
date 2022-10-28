<script>
    import { onMount } from "svelte";
    import { runningChallenge, challenges, machineSignal } from "../lib/stores"
    import Collapse from "./Collapse.svelte";
    import Loading from "./Loading.svelte";
	export let eel;
    export let selectedChallenge;

	let machines = [];
    let isStarting = false;
    let correct = false;
    let flagError = false;
    const flag_placeholder = `input with flag{___}`;

	async function list() {
        machines = [];
		machines = await eel.list_challenge_machines(selectedChallenge)();
    }

    async function start() {
        isStarting = true
        await eel.start_challenge(selectedChallenge)();
        isStarting = false
    }

    async function getNetwork() {
        const network = await eel.get_network(selectedChallenge)();
        return network
    }

    async function checkFlag(e) {
        const formData = new FormData(e.target);
        const result = await eel.compare_challenge_flag(selectedChallenge, formData.get("flag"))();
        correct = result;
        flagError = !result;
    }
    
    onMount(async () => {
        await list();
    })

    $: list(), $machineSignal;
</script>

<div class="flex flex-col gap-8 w-full">
    <div class="flex flex-row items-center">
        <!-- TITLE -->
        <h2 class="text-lg font-bold flex-1">
            TITLE: 
            <span class="font-normal">
                {$challenges[selectedChallenge].name}
            </span>
        </h2>

        <!-- HINTS -->
        <div class="flex-none">
            <div class="dropdown dropdown-left">
                <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                <div class="tooltip" data-tip="Show Hints">
                    <button tabindex="0" class="btn btn-ghost">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
                        </svg>
                    </button>
                </div>
                <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                <div tabindex="0" class="dropdown-content rounded-lg w-80 bg-slate-800 card card-compact shadow border border-primary">
                    {#each $challenges[selectedChallenge].hints as hint}
                        <Collapse title={hint.title} content={hint.content}/>
                    {/each}
                </div>
            </div>
        </div>
    </div>
    
    <!-- MACHINES -->
    <div>
        <h2 class="text-lg font-bold">MACHINES:</h2>

        <div class="mt-2 flex flex-row justify-start gap-16 p-4 card bg-slate-800 rounded-lg w-full">
            {#if machines.length > 0}
                <!-- TARGETS -->
                <ul class="flex flex-col justify-start gap-4">
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
                                <Loading></Loading>STARTING
                            {:else}
                                START MACHINES
                            {/if}
                    </button>     
                </ul>

                <!-- NETWORK -->
                {#await getNetwork() then network}
                <h2 class="text-lg font-semibold">
                    NETWORK:
                    <span class="font-normal">{network}</span>
                </h2>
                {/await}

            {:else}
                <Loading>Loading ...</Loading>
            {/if}
        </div>
    </div>

    <!-- DESCRIPTION -->
    <div>
        <h2 class="text-lg font-bold">
            DESCRIPTION:
        </h2>
        <p class="font-normal mt-2">
            {$challenges[selectedChallenge].description}
        </p>
    </div>

    <!-- FLAG -->
    <div>
        <h2 class="text-lg font-bold">
            SUBMIT THE FLAG:
        </h2>
        
            {#if correct}
                <!-- <div class="border border-green-600">  -->
                    <input disabled class="disabled:border disabled:border-green-600 w-full input input-bordered max-w-xs mt-2" placeholder="Correct!" />
                <!-- </div> -->
            {:else}
            <form on:submit|preventDefault={checkFlag}>
                <input name="flag" required type="text" placeholder={flag_placeholder} class={"active:bg-slate-700 input input-bordered w-full max-w-xs mt-2 bg-slate-700"} />
                <input type="submit" style="display: none" />
                {#if flagError}
                    <p class="text-red-400 mt-2">Flag was not correct!</p>
                {/if}
            </form>
            {/if}
    </div>

    <!-- QUIZ -->
    <div>
        <h2 class="text-lg font-bold">
            QUIZ:
        </h2>
        <ul class="mt-2 flex flex-col justify-start w-full card rounded-lg p-4 bg-slate-800">
            {#each $challenges[selectedChallenge].quiz as q}
            <li>
                <span>Question: </span>
                <span>{q}</span>
            </li>
            {/each}
        </ul>
    </div>
</div>
