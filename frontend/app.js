const API_URL = 'http://127.0.0.1:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const form = document.getElementById('prediction-form');
    const cropSelect = document.getElementById('crop');
    const soilSelect = document.getElementById('soil');
    const waterSelect = document.getElementById('water');
    const customCropGroup = document.getElementById('custom-crop-group');
    const customCropInput = document.getElementById('custom_crop');
    const logicText = document.getElementById('logic-text');
    const fertSlider = document.getElementById('fertilizer');
    const fertVal = document.getElementById('fert-val');
    const tempSlider = document.getElementById('temperature');
    const tempVal = document.getElementById('temp-val');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    const resultsContainer = document.getElementById('results-container');
    const engineStatus = document.getElementById('engine-status');

    // Fetch initial status and populate dropdowns
    fetch(`${API_URL}/status`)
        .then(res => res.json())
        .then(data => {
            if (data.engine_online) {
                engineStatus.className = 'status-indicator success';
                engineStatus.innerHTML = '✅ Core: Gradient Boosting<br><span style="font-size: 0.8rem; font-weight: normal; opacity: 0.8; margin-left: 1.5rem;">Training Accuracy: 98.9%</span>';
            } else {
                engineStatus.className = 'status-indicator error';
                engineStatus.innerHTML = '❌ Engine Fault: Training Required';
            }

            // Populate Dropdowns
            populateSelect(cropSelect, data.crop_options);
            populateSelect(soilSelect, data.soil_options);
            populateSelect(waterSelect, data.water_options);
            
            updateLogicSummary();
        })
        .catch(err => {
            engineStatus.className = 'status-indicator error';
            engineStatus.innerHTML = '❌ Backend Unreachable';
            console.error('Failed to fetch status:', err);
        });

    // Event Listeners
    cropSelect.addEventListener('change', (e) => {
        if (e.target.value === 'Other...') {
            customCropGroup.style.display = 'flex';
            customCropInput.required = true;
        } else {
            customCropGroup.style.display = 'none';
            customCropInput.required = false;
        }
        updateLogicSummary();
    });

    soilSelect.addEventListener('change', updateLogicSummary);
    waterSelect.addEventListener('change', updateLogicSummary);
    customCropInput.addEventListener('input', updateLogicSummary);

    fertSlider.addEventListener('input', (e) => fertVal.textContent = e.target.value);
    tempSlider.addEventListener('input', (e) => tempVal.textContent = e.target.value);

    // Form Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI State
        btnText.textContent = 'ANALYZING...';
        spinner.style.display = 'block';
        submitBtn.disabled = true;
        resultsContainer.style.display = 'none';

        const formData = {
            n: document.getElementById('n').value,
            p: document.getElementById('p').value,
            k: document.getElementById('k').value,
            fertilizer: fertSlider.value,
            temperature: tempSlider.value,
            crop: cropSelect.value === 'Other...' ? customCropInput.value : cropSelect.value,
            soil: soilSelect.value,
            water: waterSelect.value
        };

        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Animate count up
                animateValue(document.getElementById('final-yield'), 0, data.final_yield, 1500, ' T/HA');
                
                const appliedCrop = cropSelect.value === 'Other...' ? customCropInput.value || 'Custom Crop' : cropSelect.value;
                document.getElementById('insight-text').textContent = 
                    `Choosing ${appliedCrop} in ${soilSelect.value} conditions yields a specificity factor of ${data.specificity_factor.toFixed(2)}x.`;
                
                // Handle Warnings
                const warningsContainer = document.getElementById('warnings-container');
                warningsContainer.innerHTML = '';
                
                data.warnings.forEach(warn => {
                    const div = document.createElement('div');
                    if (warn.includes('heat')) {
                        div.className = 'warning-card red';
                        div.innerHTML = `🔥 <span>${warn}</span>`;
                    } else {
                        div.className = 'warning-card yellow';
                        div.innerHTML = `⚠️ <span>${warn}</span>`;
                    }
                    warningsContainer.appendChild(div);
                });

                resultsContainer.style.display = 'flex';
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Prediction failed:', error);
            alert('Prediction failed. Ensure the backend is running.');
        } finally {
            // Restore UI
            btnText.textContent = '✨ GENERATE SPECIFIC YIELD PREDICTION';
            spinner.style.display = 'none';
            submitBtn.disabled = false;
        }
    });

    // Helpers
    function populateSelect(selectEl, options) {
        selectEl.innerHTML = '';
        options.forEach(opt => {
            const option = document.createElement('option');
            option.value = opt;
            option.textContent = opt;
            selectEl.appendChild(option);
        });
    }

    function updateLogicSummary() {
        const crop = cropSelect.value === 'Other...' ? (customCropInput.value || 'Custom Crop') : cropSelect.value;
        const soil = soilSelect.value;
        const water = waterSelect.value;
        
        if(crop && soil && water) {
            logicText.textContent = `Targeting ${crop} in ${soil} soil with ${water} strategy.`;
        }
    }

    // Number animation
    function animateValue(obj, start, end, duration, suffix = '') {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            // Ease out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentVal = (start + (end - start) * easeOut).toFixed(3);
            obj.innerHTML = `${currentVal}<span>${suffix}</span>`;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                obj.innerHTML = `${end.toFixed(3)}<span>${suffix}</span>`;
            }
        };
        window.requestAnimationFrame(step);
    }
});
