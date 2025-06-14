<script lang="ts">
  import { onMount } from 'svelte';
  import { toast } from 'svelte-sonner';
  import { getModels } from '$lib/apis'; // Import from $lib/apis
  import { createAgent } from '$lib/apis/agents';
  import { user } from '$lib/stores';

  let agentName = '';
  let agentRole = '';
  let systemMessage = '';
  let skills = '';
  let availableModels = [];
  let selectedModel = '';
  let loadingModels = true; // Added loadingModels state

  onMount(async () => {
    loadingModels = true; 
    try {
      const modelsArray = await getModels($user.token); // Call getModels from $lib/apis

      if (modelsArray && Array.isArray(modelsArray)) {
        if (modelsArray.length === 0) {
          console.log("No models available. The list from API is empty.");
          toast.info("No models available to select.");
          availableModels = [];
          selectedModel = '';
        } else {
          availableModels = modelsArray.map((model) => ({
            id: model.id, 
            name: model.name,
          }));
          selectedModel = availableModels[0].id;
        }
      } else {
        // This case means modelsArray is null (due to an error in getModels) or not an array
        console.error("Invalid model data received or error in getModels:", modelsArray);
        toast.error("Error: Could not parse model list from the server.");
        availableModels = [];
        selectedModel = '';
      }
    } catch (error) {
      toast.error(`Error fetching available models: ${error.message}`);
      console.error('Error fetching available models:', error);
      availableModels = [];
      selectedModel = '';
    } finally {
      loadingModels = false;
    }
  });

  async function handleSubmit() {
    const agentData = {
      name: agentName,
      role: agentRole,
      system_message: systemMessage || null,
      model_id: selectedModel, // Changed from llm_model to model_id
      skills: skills || null, // Send skills as a string
    };

    try {
      const response = await createAgent($user.token, agentData);
      toast.success(`Agent "${response.name}" created successfully!`);
      // Optionally, clear the form or redirect
      agentName = '';
      agentRole = '';
      systemMessage = '';
      skills = '';
      // selectedModel remains as is, or you can reset it to the default
    } catch (error) {
      toast.error(`Error creating agent: ${error}`);
      console.error('Error creating agent:', error);
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4">
  <div>
    <label for="agentName" class="block text-sm font-medium text-gray-700">Agent Name</label>
    <input type="text" id="agentName" bind:value={agentName} class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
  </div>

  <div>
    <label for="llmModel" class="block text-sm font-medium text-gray-700">LLM Model</label>
    <select id="llmModel" bind:value={selectedModel} class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" disabled={loadingModels || availableModels.length === 0}>
      {#if loadingModels}
        <option value="" disabled>Loading models...</option>
      {:else if availableModels.length === 0}
        <option value="" disabled>No models available</option>
      {:else}
        {#each availableModels as model}
          <option value={model.id}>{model.name}</option>
        {/each}
      {/if}
    </select>
  </div>

  <div>
    <label for="agentRole" class="block text-sm font-medium text-gray-700">Agent Role</label>
    <textarea id="agentRole" bind:value={agentRole} rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"></textarea>
  </div>

  <div>
    <label for="systemMessage" class="block text-sm font-medium text-gray-700">System Message</label>
    <textarea id="systemMessage" bind:value={systemMessage} rows="5" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"></textarea>
  </div>

  <div>
    <label for="skills" class="block text-sm font-medium text-gray-700">Skills</label>
    <textarea id="skills" bind:value={skills} rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" placeholder="Enter skills, separated by commas"></textarea>
  </div>

  <div>
    <button type="submit" class="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
      Create Agent
    </button>
  </div>
</form>
