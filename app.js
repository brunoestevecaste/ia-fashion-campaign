const API = {
  createCampaign: "/api/campaigns",
  campaignStatus: (jobId) => `/api/campaigns/${jobId}/status`,
  campaignResult: (jobId) => `/api/campaigns/${jobId}/result`,
};

const presetData = {
  styles: [
    {
      name: "Luxury Editorial Minimalism",
      text:
        "Luxury high-fashion editorial styling with clean visual hierarchy, restrained elegance and magazine-grade refinement focused on exclusivity.",
    },
    {
      name: "Avant-Garde Couture Drama",
      text:
        "Avant-garde couture styling with sculptural silhouettes, experimental layering and runway-level visual tension.",
    },
    {
      name: "90s Supermodel Power",
      text:
        "Iconic 90s supermodel styling with commanding pose language, strong attitude and glossy magazine polish.",
    },
    {
      name: "Contemporary Quiet Luxury",
      text:
        "Quiet-luxury styling with tactile premium fabrics, muted tonal harmony and refined restraint.",
    },
    {
      name: "Cinematic Urban Glamour",
      text:
        "Cinematic urban glamour with premium street-luxury combinations, dynamic movement and magazine-ready energy.",
    },
  ],
  locations: [
    {
      name: "Sunset Rooftop Skyline",
      text:
        "High rooftop at sunset above a dense metropolitan skyline, with concrete textures, railings and layered atmospheric urban depth.",
    },
    {
      name: "Brutalist Museum Forecourt",
      text:
        "Open-air brutalist museum forecourt with monumental concrete geometry and sculpted shadows.",
    },
    {
      name: "Historic European Avenue",
      text:
        "Historic European avenue with classic facades, stone pavement and soft natural light across architectural surfaces.",
    },
    {
      name: "Art Deco Hotel Lobby",
      text:
        "Grand art deco hotel lobby with geometric symmetry, brass accents and layered architectural depth.",
    },
    {
      name: "Tokyo Neon Backstreet",
      text:
        "Narrow Tokyo backstreet at blue hour with neon glow, wet reflections and dense urban perspective.",
    },
  ],
  models: [
    {
      name: "Freckled Natural Muse",
      text:
        "Young woman with radiant, natural beauty, hazel-green eyes, soft freckles and black curls with platinum undertones.",
    },
    {
      name: "Androgynous Runway Edge",
      text:
        "Young androgynous model with sharp jawline, high cheekbones, neutral warm skin tone and short brushed-back dark hair.",
    },
    {
      name: "Mediterranean Classic Beauty",
      text:
        "Young woman with olive skin, hazel eyes, thick dark eyebrows and long glossy chestnut hair.",
    },
    {
      name: "Latin Curly Glamour",
      text:
        "Young Latina model with warm golden-olive skin, expressive brown eyes and long dark brown curls.",
    },
    {
      name: "Classic Tailored Male Lead",
      text:
        "Young man with defined jawline, medium-light warm skin tone, deep brown eyes and neatly textured dark hair.",
    },
  ],
  defaults: {
    style:
      "Photorealistic high-fashion campaign with luxury editorial direction, refined cinematic color grading and elegant visual storytelling.",
    location:
      "A high rooftop at sunset above a dense city skyline, with warm low-angle sunlight and atmospheric haze for hyperrealistic editorial photography.",
    model:
      "Young woman with radiant natural beauty, delicate freckles, hazel-green eyes, soft pink lips and voluminous black curls with platinum undertones.",
  },
};

const STYLE_MODE_LABELS = {
  preset: "Preset optimizado",
  custom: "Prompt personalizado",
};

const LOCATION_MODE_LABELS = {
  preset: "Preset optimizado",
  custom: "Prompt personalizado",
};

const MODEL_MODE_LABELS = {
  preset: "Preset de descripcion",
  custom: "Descripcion personalizada",
  upload: "Subir imagen del modelo",
};

const state = {
  isGenerating: false,
  currentJobId: "",
  uploadUrls: {
    garment: "",
    model: "",
  },
  result: null,
};

const elements = {
  form: document.getElementById("campaign-form"),
  results: document.getElementById("results"),
  promptsList: document.getElementById("prompts-list"),
  galleryGrid: document.getElementById("gallery-grid"),
  downloadZip: document.getElementById("download-zip"),
  modelReferenceImage: document.getElementById("model-reference-image"),
  statusPill: document.getElementById("status-pill"),
  progressFill: document.getElementById("progress-fill"),
  logList: document.getElementById("log-list"),
  generateButton: document.getElementById("generate-button"),
  garmentPreviewImage: document.getElementById("garment-preview-image"),
  garmentPreviewPlaceholder: document.getElementById("garment-preview-placeholder"),
  modelPreviewImage: document.getElementById("model-preview-image"),
  modelPreviewPlaceholder: document.getElementById("model-preview-placeholder"),
  garmentFileMeta: document.getElementById("garment-file-meta"),
  modelFileMeta: document.getElementById("model-file-meta"),
  summaryRender: document.getElementById("summary-render"),
  summaryCount: document.getElementById("summary-count"),
  summaryStyle: document.getElementById("summary-style"),
  summaryModel: document.getElementById("summary-model"),
  apiKeyField: document.getElementById("field-api-key"),
  garmentField: document.getElementById("field-garment-file"),
  modelFileField: document.getElementById("field-model-file"),
};

document.addEventListener("DOMContentLoaded", init);

function init() {
  populateSelect(document.getElementById("style-preset"), presetData.styles);
  populateSelect(document.getElementById("location-preset"), presetData.locations);
  populateSelect(document.getElementById("model-preset"), presetData.models);

  document.getElementById("style-custom").value = presetData.defaults.style;
  document.getElementById("location-custom").value = presetData.defaults.location;
  document.getElementById("model-custom").value = presetData.defaults.model;

  bindEvents();
  syncModePanels();
  updateSummary();
  refreshPreviewPanels();
  setStatus("idle", "Idle");
  writeLogs(["Esperando configuracion creativa."]);
}

function bindEvents() {
  elements.form.addEventListener("change", (event) => {
    if (event.target instanceof HTMLInputElement && event.target.type === "file") {
      handleFileInputChange(event.target);
    }
    syncModePanels();
    updateSummary();
    refreshPreviewPanels();
    clearFieldErrorForTarget(event.target);
  });

  elements.form.addEventListener("input", (event) => {
    clearFieldErrorForTarget(event.target);
    updateSummary();
    refreshPreviewPanels();
  });

  elements.form.addEventListener("submit", async (event) => {
    event.preventDefault();
    await handleGenerate();
  });

  elements.downloadZip.addEventListener("click", () => {
    if (!state.result) {
      return;
    }
    downloadFromUrl(state.result.downloadZipUrl, "fashion_campaign_complete.zip");
  });

  window.addEventListener("beforeunload", cleanupObjectUrls);
}

function populateSelect(select, items) {
  const fragment = document.createDocumentFragment();
  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.name;
    option.textContent = item.name;
    fragment.appendChild(option);
  });
  select.innerHTML = "";
  select.appendChild(fragment);
}

function syncModePanels() {
  const values = getControlValues();
  togglePanels("style", values.styleMode);
  togglePanels("location", values.locationMode);
  togglePanels("model", values.modelMode);
}

function togglePanels(panelName, activeValue) {
  document.querySelectorAll(`[data-panel="${panelName}"]`).forEach((panel) => {
    panel.hidden = panel.dataset.value !== activeValue;
  });
}

function getControlValues() {
  return {
    renderMode: getCheckedValue("renderMode"),
    styleMode: getCheckedValue("styleMode"),
    locationMode: getCheckedValue("locationMode"),
    modelMode: getCheckedValue("modelMode"),
  };
}

function getCheckedValue(name) {
  const checked = elements.form.querySelector(`input[name="${name}"]:checked`);
  return checked ? checked.value : "";
}

function handleFileInputChange(input) {
  if (input.id === "garment-file") {
    updateUploadUrl("garment", input.files && input.files[0] ? URL.createObjectURL(input.files[0]) : "");
    elements.garmentFileMeta.textContent =
      input.files && input.files[0] ? input.files[0].name : "JPG, PNG o WEBP";
  }

  if (input.id === "model-file") {
    updateUploadUrl("model", input.files && input.files[0] ? URL.createObjectURL(input.files[0]) : "");
    elements.modelFileMeta.textContent =
      input.files && input.files[0] ? input.files[0].name : "Se usara como base de consistencia visual";
  }
}

function updateUploadUrl(key, nextUrl) {
  if (state.uploadUrls[key]) {
    URL.revokeObjectURL(state.uploadUrls[key]);
  }
  state.uploadUrls[key] = nextUrl;
}

function refreshPreviewPanels() {
  refreshGarmentPreview();
  refreshModelPreview();
}

function refreshGarmentPreview() {
  if (state.uploadUrls.garment) {
    elements.garmentPreviewImage.src = state.uploadUrls.garment;
    elements.garmentPreviewImage.hidden = false;
    elements.garmentPreviewPlaceholder.classList.add("is-hidden");
    return;
  }

  elements.garmentPreviewImage.hidden = true;
  elements.garmentPreviewPlaceholder.classList.remove("is-hidden");
}

function refreshModelPreview() {
  const payload = collectPayload();

  if (payload.modelModeValue === "upload" && state.uploadUrls.model) {
    elements.modelPreviewImage.src = state.uploadUrls.model;
    elements.modelPreviewImage.hidden = false;
    elements.modelPreviewPlaceholder.classList.add("is-hidden");
    return;
  }

  const descriptor = payload.modelModeValue === "preset" ? payload.modelLabel : payload.modelDescriptor;
  const svg = createModelReferenceSvg({
    title: descriptor || "Model reference",
    subtitle: payload.modelModeValue === "custom" ? "Descripcion personalizada" : "Reference profile",
  });
  elements.modelPreviewImage.src = svgToDataUrl(svg);
  elements.modelPreviewImage.hidden = false;
  elements.modelPreviewPlaceholder.classList.add("is-hidden");
}

function collectPayload() {
  const values = getControlValues();
  const garmentFile = elements.form.elements.garmentFile.files[0] || null;
  const modelFile = elements.form.elements.modelFile.files[0] || null;
  const stylePreset = findPreset(presetData.styles, elements.form.elements.stylePreset.value);
  const locationPreset = findPreset(presetData.locations, elements.form.elements.locationPreset.value);
  const modelPreset = findPreset(presetData.models, elements.form.elements.modelPreset.value);

  const styleDescriptor =
    values.styleMode === "preset"
      ? stylePreset.text
      : elements.form.elements.styleCustom.value.trim();
  const locationDescriptor =
    values.locationMode === "preset"
      ? locationPreset.text
      : elements.form.elements.locationCustom.value.trim();
  const modelDescriptor =
    values.modelMode === "preset"
      ? modelPreset.text
      : values.modelMode === "custom"
        ? elements.form.elements.modelCustom.value.trim()
        : "";

  return {
    apiKey: elements.form.elements.apiKey.value.trim(),
    garmentFile,
    renderMode: values.renderMode,
    styleModeValue: values.styleMode,
    styleModeLabel: STYLE_MODE_LABELS[values.styleMode],
    styleLabel: values.styleMode === "preset" ? stylePreset.name : "Custom",
    styleDescriptor,
    locationModeValue: values.locationMode,
    locationModeLabel: LOCATION_MODE_LABELS[values.locationMode],
    locationLabel: values.locationMode === "preset" ? locationPreset.name : "Custom",
    locationDescriptor,
    modelModeValue: values.modelMode,
    modelModeLabel: MODEL_MODE_LABELS[values.modelMode],
    modelLabel:
      values.modelMode === "preset"
        ? modelPreset.name
        : values.modelMode === "upload"
          ? "Imagen subida"
          : "Custom",
    modelDescriptor,
    modelFile,
  };
}

function findPreset(items, name) {
  return items.find((item) => item.name === name) || items[0];
}

function updateSummary() {
  const payload = collectPayload();
  elements.summaryRender.textContent = payload.renderMode;
  elements.summaryCount.textContent = payload.renderMode === "Final" ? "4" : "2";
  elements.summaryStyle.textContent = payload.styleModeValue === "preset" ? payload.styleLabel : "Custom";
  elements.summaryModel.textContent =
    payload.modelModeValue === "preset"
      ? payload.modelLabel
      : payload.modelModeValue === "upload"
        ? "Upload"
        : "Custom";
}

async function handleGenerate() {
  if (state.isGenerating) {
    return;
  }

  const payload = collectPayload();
  clearAllErrors();

  if (!validatePayload(payload)) {
    setStatus("error", "Revisa el formulario");
    writeLogs(["Faltan campos obligatorios. Corrige los errores resaltados para continuar."]);
    return;
  }

  state.isGenerating = true;
  state.result = null;
  state.currentJobId = "";
  updateGenerateButton();
  elements.results.hidden = true;
  setStatus("running", "Submitting");
  setProgress(4);
  writeLogs(["Enviando configuracion creativa al backend de Python..."]);

  try {
    const response = await createCampaign(payload);
    state.currentJobId = response.jobId;
    await pollCampaign(response.jobId);
  } catch (error) {
    console.error(error);
    setStatus("error", "Error");
    writeLogs([error.message || "No se pudo completar el shooting."]);
  } finally {
    state.isGenerating = false;
    updateGenerateButton();
  }
}

function validatePayload(payload) {
  let valid = true;

  if (!payload.apiKey) {
    setFieldError(elements.apiKeyField, "Introduce una Google API Key.");
    valid = false;
  }

  if (!payload.garmentFile) {
    setFieldError(elements.garmentField, "Debes subir una fotografia de la prenda.");
    valid = false;
  }

  if (payload.styleModeValue === "custom" && !payload.styleDescriptor) {
    setFieldError(document.getElementById("style-custom").closest(".field"), "Escribe un prompt de estilo.");
    valid = false;
  }

  if (payload.locationModeValue === "custom" && !payload.locationDescriptor) {
    setFieldError(
      document.getElementById("location-custom").closest(".field"),
      "Escribe un prompt de ubicacion."
    );
    valid = false;
  }

  if (payload.modelModeValue === "custom" && !payload.modelDescriptor) {
    setFieldError(
      document.getElementById("model-custom").closest(".field"),
      "Escribe una descripcion del modelo."
    );
    valid = false;
  }

  if (payload.modelModeValue === "upload" && !payload.modelFile) {
    setFieldError(elements.modelFileField, "Debes subir una imagen del modelo.");
    valid = false;
  }

  return valid;
}

async function createCampaign(payload) {
  const formData = new FormData();
  formData.append("apiKey", payload.apiKey);
  formData.append("renderMode", payload.renderMode);
  formData.append("styleMode", payload.styleModeLabel);
  formData.append("styleDesc", payload.styleDescriptor);
  formData.append("locationMode", payload.locationModeLabel);
  formData.append("locationDesc", payload.locationDescriptor);
  formData.append("modelMode", payload.modelModeLabel);
  formData.append("modelDesc", payload.modelDescriptor);
  formData.append("garmentFile", payload.garmentFile);
  if (payload.modelFile) {
    formData.append("modelFile", payload.modelFile);
  }

  const response = await fetch(API.createCampaign, {
    method: "POST",
    body: formData,
  });
  const data = await parseJsonResponse(response);

  if (!response.ok) {
    if (Array.isArray(data.missingFields)) {
      applyMissingFieldErrors(data.missingFields);
      throw new Error(`Faltan campos obligatorios: ${data.missingFields.join(", ")}.`);
    }
    throw new Error(data.error || "El backend rechazo la solicitud.");
  }

  return data;
}

async function pollCampaign(jobId) {
  while (true) {
    const response = await fetch(`${API.campaignStatus(jobId)}?t=${Date.now()}`, {
      cache: "no-store",
    });
    const data = await parseJsonResponse(response);

    if (!response.ok) {
      throw new Error(data.error || "No se pudo consultar el estado del pipeline.");
    }

    updateStatusPanel(data);

    if (data.state === "complete") {
      const result = await fetchCampaignResult(jobId);
      state.result = result;
      renderResults(result);
      setStatus("success", "Complete");
      setProgress(100);
      return;
    }

    if (data.state === "error") {
      throw new Error(data.error || "No se pudo completar el shooting.");
    }

    await wait(1200);
  }
}

async function fetchCampaignResult(jobId) {
  const response = await fetch(`${API.campaignResult(jobId)}?t=${Date.now()}`, {
    cache: "no-store",
  });
  const data = await parseJsonResponse(response);

  if (!response.ok) {
    throw new Error(data.error || "No se pudo recuperar el resultado del shooting.");
  }

  return data;
}

function updateStatusPanel(snapshot) {
  const logs = Array.isArray(snapshot.logs) && snapshot.logs.length > 0
    ? snapshot.logs
    : ["Esperando configuracion creativa."];

  writeLogs(logs);
  setProgress(Number.isFinite(snapshot.progress) ? snapshot.progress : 0);

  if (snapshot.state === "queued") {
    setStatus("running", "Queued");
    return;
  }

  if (snapshot.state === "running") {
    setStatus("running", "Running");
    return;
  }

  if (snapshot.state === "complete") {
    setStatus("success", "Complete");
    return;
  }

  if (snapshot.state === "error") {
    setStatus("error", "Error");
  }
}

function renderResults(result) {
  renderPromptList(result.prompts);
  renderModelReference(result.modelReferenceUrl);
  renderGallery(result.images);
  elements.results.hidden = false;
}

function renderPromptList(prompts) {
  elements.promptsList.innerHTML = "";
  prompts.forEach((prompt, index) => {
    const item = document.createElement("li");
    item.innerHTML = `<strong>Prompt ${index + 1}</strong><span>${escapeHtml(prompt)}</span>`;
    elements.promptsList.appendChild(item);
  });
}

function renderModelReference(sourceUrl) {
  elements.modelReferenceImage.src = sourceUrl;
}

function renderGallery(images) {
  elements.galleryGrid.innerHTML = "";

  images.forEach((image) => {
    const card = document.createElement("article");
    card.className = "gallery-card";
    card.innerHTML = `
      <div class="gallery-card__frame">
        <img src="${image.url}" alt="${image.title}" />
      </div>
      <div class="gallery-card__meta">
        <div>
          <span class="gallery-card__title">${escapeHtml(image.title)}</span>
          <span class="gallery-card__subtitle">${escapeHtml(image.subtitle)}</span>
        </div>
        <button class="button button--secondary" type="button" data-download-url="${image.downloadUrl}" data-filename="${image.filename}">
          Descargar
        </button>
      </div>
    `;
    elements.galleryGrid.appendChild(card);
  });

  elements.galleryGrid.querySelectorAll("[data-download-url]").forEach((button) => {
    button.addEventListener("click", () => {
      downloadFromUrl(button.dataset.downloadUrl, button.dataset.filename);
    });
  });
}

function clearAllErrors() {
  elements.form.querySelectorAll(".field").forEach((field) => {
    field.classList.remove("is-invalid");
    const error = field.querySelector(".field__error");
    if (error) {
      error.textContent = "";
    }
  });
}

function clearFieldErrorForTarget(target) {
  if (!(target instanceof HTMLElement)) {
    return;
  }

  const field = target.closest(".field");
  if (!field) {
    return;
  }

  field.classList.remove("is-invalid");
  const error = field.querySelector(".field__error");
  if (error) {
    error.textContent = "";
  }
}

function setFieldError(field, message) {
  if (!field) {
    return;
  }

  field.classList.add("is-invalid");
  const error = field.querySelector(".field__error");
  if (error) {
    error.textContent = message;
  }
}

function applyMissingFieldErrors(missingFields) {
  const fieldMap = {
    "API key de Google": [elements.apiKeyField, "Introduce una Google API Key."],
    "fotografia de la prenda": [elements.garmentField, "Debes subir una fotografia de la prenda."],
    "descripcion del estilo": [
      document.getElementById("style-custom").closest(".field"),
      "Escribe un prompt de estilo.",
    ],
    "descripcion de la ubicacion": [
      document.getElementById("location-custom").closest(".field"),
      "Escribe un prompt de ubicacion.",
    ],
    "descripcion fisica del modelo": [
      document.getElementById("model-custom").closest(".field"),
      "Escribe una descripcion del modelo.",
    ],
    "imagen del modelo": [elements.modelFileField, "Debes subir una imagen del modelo."],
  };

  missingFields.forEach((fieldName) => {
    const entry = fieldMap[fieldName];
    if (entry) {
      setFieldError(entry[0], entry[1]);
    }
  });
}

function setStatus(kind, label) {
  elements.statusPill.textContent = label;
  elements.statusPill.classList.remove("is-running", "is-success", "is-error");

  if (kind === "running") {
    elements.statusPill.classList.add("is-running");
  } else if (kind === "success") {
    elements.statusPill.classList.add("is-success");
  } else if (kind === "error") {
    elements.statusPill.classList.add("is-error");
  }
}

function setProgress(value) {
  elements.progressFill.style.width = `${Math.max(0, Math.min(100, value))}%`;
}

function writeLogs(lines) {
  elements.logList.innerHTML = "";
  lines.forEach((line) => {
    const item = document.createElement("li");
    item.textContent = line;
    elements.logList.appendChild(item);
  });
}

function updateGenerateButton() {
  const label = elements.generateButton.querySelector(".button__label");
  elements.generateButton.disabled = state.isGenerating;
  label.textContent = state.isGenerating ? "Generando..." : "Generar shooting";
}

async function parseJsonResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }

  const text = await response.text();
  return text ? { error: text } : {};
}

function downloadFromUrl(url, filename) {
  const anchor = document.createElement("a");
  anchor.href = url;
  if (filename) {
    anchor.download = filename;
  }
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
}

function cleanupObjectUrls() {
  Object.values(state.uploadUrls).forEach((url) => {
    if (url) {
      URL.revokeObjectURL(url);
    }
  });
}

function wait(ms) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

function createModelReferenceSvg({ title, subtitle }) {
  return `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200">
      <defs>
        <linearGradient id="g" x1="0%" x2="100%" y1="0%" y2="100%">
          <stop offset="0%" stop-color="#323944" />
          <stop offset="48%" stop-color="#8b1616" />
          <stop offset="100%" stop-color="#c7aea1" />
        </linearGradient>
        <radialGradient id="r" cx="50%" cy="20%" r="68%">
          <stop offset="0%" stop-color="rgba(251,244,242,0.9)" />
          <stop offset="100%" stop-color="rgba(251,244,242,0)" />
        </radialGradient>
      </defs>
      <rect width="1200" height="1200" fill="url(#g)" />
      <circle cx="600" cy="250" r="180" fill="url(#r)" opacity="0.45" />
      <circle cx="600" cy="445" r="180" fill="#fbf4f2" opacity="0.18" />
      <rect x="375" y="610" width="450" height="360" rx="220" fill="#fbf4f2" opacity="0.12" />
      <rect x="78" y="78" width="1044" height="1044" rx="54" fill="none" stroke="rgba(251,244,242,0.18)" stroke-width="2" />
      <text x="104" y="145" fill="#fbf4f2" font-size="42" letter-spacing="10" style="font-family: Arial, sans-serif;">MODEL REFERENCE</text>
      <text x="104" y="928" fill="#fbf4f2" font-size="80" style="font-family: Georgia, serif;">${escapeXml(
        title
      )}</text>
      <text x="104" y="994" fill="#fbf4f2" opacity="0.72" font-size="32" style="font-family: Arial, sans-serif;">${escapeXml(
        subtitle
      )}</text>
    </svg>
  `;
}

function svgToDataUrl(svg) {
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeXml(value) {
  return escapeHtml(value);
}
