const CARD_VERSION = "1.0.0";

function _wordmarkUrl() {
  return "/crystal_water_monitor/CWM_icon_wordmark_color.svg";
}

// --- Editor ---

class CrystalDiscCardEditor extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    const selector = this.shadowRoot?.querySelector("ha-selector");
    if (selector) selector.hass = hass;
  }

  setConfig(config) {
    this._config = config;
    this._render();
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <style>
        .row { padding: 8px 0; }
        .checkbox-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; font-size: 14px; }
        .checkbox-row label { cursor: pointer; }
      </style>
      <div class="row">
        <ha-selector label="Vessel"></ha-selector>
      </div>
      <div class="checkbox-row">
        <input type="checkbox" id="transparent" ${this._config?.transparent ? "checked" : ""} />
        <label for="transparent">Transparent background</label>
      </div>
    `;

    const selector = this.shadowRoot.querySelector("ha-selector");
    if (this._hass) selector.hass = this._hass;
    selector.selector = { device: { integration: "crystal_water_monitor" } };
    selector.value = this._config?.device_id || "";
    selector.label = "Vessel";

    selector.addEventListener("value-changed", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, device_id: e.detail.value } },
        bubbles: true,
        composed: true,
      }));
    });

    this.shadowRoot.querySelector("#transparent").addEventListener("change", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, transparent: e.target.checked } },
        bubbles: true,
        composed: true,
      }));
    });
  }
}

customElements.define("crystal-disc-card-editor", CrystalDiscCardEditor);

// --- Card ---

class CrystalDiscCard extends HTMLElement {
  static getConfigElement() {
    return document.createElement("crystal-disc-card-editor");
  }

  static getStubConfig() {
    return { device_id: "", transparent: false };
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 3;
  }

  _findWaterStatusEntity() {
    if (!this._hass || !this._config?.device_id) return null;
    const deviceId = this._config.device_id;
    return Object.values(this._hass.states).find((state) => {
      const entityDeviceId = this._hass.entities?.[state.entity_id]?.device_id;
      return entityDeviceId === deviceId && state.entity_id.endsWith("_water_status");
    });
  }

  _discUrl(color) {
    const name = ["blue", "orange", "red", "gray"].includes(color) ? color : "blue";
    return `/crystal_water_monitor/disc-${name}.svg`;
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });

    const entity = this._findWaterStatusEntity();
    const transparent = this._config?.transparent;

    if (!entity) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div style="padding:16px;color:var(--secondary-text-color)">
            ${this._config?.device_id ? "Water Status entity not found for this vessel." : "Select a vessel in the card editor."}
          </div>
        </ha-card>`;
      return;
    }

    const disc = entity.attributes;
    const color = disc.waterStatusColor || "gray";
    const discUrl = this._discUrl(color);
    const name = disc.name || entity.attributes.friendly_name || "";
    const text = disc.text || entity.state || "";
    const lastUpdated = disc.lastUpdatedText || disc.last_updated_text || "";
    const tempC = disc.tempC;
    const tempF = tempC != null ? ((tempC * 9) / 5 + 32).toFixed(0) : null;
    const temp = tempF != null ? `${tempF}°F` : "";

    const inner = `
      <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 24px;
      ">
        <div style="position: relative; width: 240px; height: 240px;">
          <img src="${discUrl}" style="width: 100%; height: 100%;" />
          <div style="
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
            padding: 40px;
            box-sizing: border-box;
          ">
            <div style="font-size: 13px; font-weight: 600; margin-bottom: 6px;">${name}</div>
            <div style="font-size: 44px; font-weight: 700; line-height: 1;">${temp}</div>
            <div style="font-size: 13px; margin-top: 6px;">${text}</div>
            <div style="font-size: 11px; margin-top: 10px; opacity: 0.85;">${lastUpdated}</div>
          </div>
        </div>

      </div>
    `;

    if (transparent) {
      this.shadowRoot.innerHTML = `<div style="background:transparent;">${inner}</div>`;
    } else {
      this.shadowRoot.innerHTML = `<ha-card>${inner}</ha-card>`;
    }
  }
}

customElements.define("crystal-disc-card", CrystalDiscCard);

// --- Actions Card Editor ---

class CrystalActionsCardEditor extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    const selector = this.shadowRoot?.querySelector("ha-selector");
    if (selector) selector.hass = hass;
  }

  setConfig(config) {
    this._config = config;
    this._render();
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <style>
        .checkbox-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; font-size: 14px; }
        .checkbox-row label { cursor: pointer; }
      </style>
      <div style="padding:8px 0"><ha-selector label="Vessel"></ha-selector></div>
      <div class="checkbox-row">
        <input type="checkbox" id="show_details" ${this._config?.show_details !== false ? "checked" : ""} />
        <label for="show_details">Show description</label>
      </div>
      <div class="checkbox-row">
        <input type="checkbox" id="show_logo" ${this._config?.show_logo !== false ? "checked" : ""} />
        <label for="show_logo">Show logo</label>
      </div>
    `;
    const selector = this.shadowRoot.querySelector("ha-selector");
    if (this._hass) selector.hass = this._hass;
    selector.selector = { device: { integration: "crystal_water_monitor" } };
    selector.value = this._config?.device_id || "";
    selector.label = "Vessel";
    selector.addEventListener("value-changed", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, device_id: e.detail.value } },
        bubbles: true,
        composed: true,
      }));
    });
    this.shadowRoot.querySelector("#show_details").addEventListener("change", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, show_details: e.target.checked } },
        bubbles: true,
        composed: true,
      }));
    });
    this.shadowRoot.querySelector("#show_logo").addEventListener("change", (e) => {
      this.dispatchEvent(new CustomEvent("config-changed", {
        detail: { config: { ...this._config, show_logo: e.target.checked } },
        bubbles: true,
        composed: true,
      }));
    });
  }
}

customElements.define("crystal-actions-card-editor", CrystalActionsCardEditor);

// --- Actions Card ---

class CrystalActionsCard extends HTMLElement {
  static getConfigElement() {
    return document.createElement("crystal-actions-card-editor");
  }

  static getStubConfig() {
    return { device_id: "", show_details: true };
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 3;
  }

  _findWaterStatusEntity() {
    if (!this._hass || !this._config?.device_id) return null;
    const deviceId = this._config.device_id;
    return Object.values(this._hass.states).find((state) => {
      const entityDeviceId = this._hass.entities?.[state.entity_id]?.device_id;
      return entityDeviceId === deviceId && state.entity_id.endsWith("_water_status");
    });
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });

    const entity = this._findWaterStatusEntity();

    if (!entity) {
      this.shadowRoot.innerHTML = `
        <ha-card>
          <div style="padding:16px;color:var(--secondary-text-color)">
            ${this._config?.device_id ? "Entity not found for this vessel." : "Select a vessel in the card editor."}
          </div>
        </ha-card>`;
      return;
    }

    const actions = entity.attributes.actions || [];
    const vesselName = entity.attributes.name || "";
    const showDetails = this._config?.show_details !== false;
    const showLogo = this._config?.show_logo !== false;

    const rows = actions.length === 0
      ? `<div style="padding:16px;color:var(--secondary-text-color)">No actions needed.</div>`
      : actions.map((a) => `
          <div style="
            display: flex;
            align-items: center;
            padding: 12px 16px;
            border-bottom: 1px solid var(--divider-color);
            gap: 12px;
          ">
            ${a.iconUrl ? `<img src="${a.iconUrl}" style="width:36px;height:36px;border-radius:50%;flex-shrink:0;" />` : ""}
            <div>
              <div style="font-size:14px;font-weight:600;">${a.title || ""}</div>
              ${showDetails && a.details ? `<div style="font-size:12px;color:var(--secondary-text-color);margin-top:2px;">${a.details}</div>` : ""}
            </div>
          </div>
        `).join("");

    this.shadowRoot.innerHTML = `
      <ha-card>
        <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;">
          <div style="font-size:13px;font-weight:600;color:var(--secondary-text-color);text-transform:uppercase;letter-spacing:0.05em;">${vesselName} Actions</div>
          ${showLogo ? `<img src="${_wordmarkUrl()}" style="height:30px;" />` : ""}
        </div>
        ${rows}
      </ha-card>
    `;
  }
}

customElements.define("crystal-actions-card", CrystalActionsCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "crystal-disc-card",
  name: "Crystal Disc",
  description: "Water status disc for Crystal Water Monitor",
});
window.customCards.push({
  type: "crystal-actions-card",
  name: "Crystal Actions",
  description: "Recommended actions for a Crystal Water Monitor vessel",
});

console.info(`%c CRYSTAL-DISC-CARD %c ${CARD_VERSION} `, "color:white;background:#2d7fc1;font-weight:700", "color:#2d7fc1;background:white;font-weight:700");
