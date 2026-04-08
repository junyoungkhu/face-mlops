document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const timetableBtn = document.getElementById('search-timetable-btn');
    const routeSelect = document.getElementById('route-select');
    const timetableResults = document.getElementById('timetable-results');
    
    const predictBtn = document.getElementById('predict-btn');
    const stopSelect = document.getElementById('stop-select');
    const timeSelect = document.getElementById('time-select');
    const predictionResult = document.getElementById('prediction-result');
    
    const loadingOverlay = document.getElementById('loading-overlay');

    // Utility: Show/Hide Loader
    const toggleLoader = (show) => {
        if (show) loadingOverlay.classList.remove('hidden');
        else loadingOverlay.classList.add('hidden');
    };

    // 1. Fetch Timetable
    timetableBtn.addEventListener('click', async () => {
        const routeId = routeSelect.value;
        toggleLoader(true);
        
        try {
            // Simulated API Delay for UX
            await new Promise(r => setTimeout(r, 600));

            const response = await fetch(`/api/v1/shuttle/timetable/${encodeURIComponent(routeId)}`);
            if (!response.ok) throw new Error('API Error');
            const data = await response.json();
            
            timetableResults.innerHTML = ''; // clear
            
            if (data.length === 0) {
                timetableResults.innerHTML = `<p class="empty-state">해당 노선의 시간표가 없습니다.</p>`;
                return;
            }

            // Render cards
            data.forEach(bus => {
                const row = document.createElement('div');
                row.className = 'time-row';
                row.innerHTML = `
                    <div class="bus-id">${bus.bus_id}</div>
                    <div class="time-details">
                        <div class="time-point time-dep">
                            <i data-lucide="log-out"></i>
                            <span>${bus.departure_time}</span>
                        </div>
                        <div class="time-point time-arr">
                            <i data-lucide="log-in"></i>
                            <span>${bus.arrival_time}</span>
                        </div>
                    </div>
                `;
                timetableResults.appendChild(row);
            });
            
            // Re-init icons
            lucide.createIcons();

        } catch (error) {
            console.error(error);
            timetableResults.innerHTML = `<p class="empty-state" style="color:var(--danger)">데이터를 불러오는데 실패했습니다.</p>`;
        } finally {
            toggleLoader(false);
        }
    });

    // 2. Fetch Boarding Prediction
    predictBtn.addEventListener('click', async () => {
        const stopName = stopSelect.value;
        const timeOfDay = timeSelect.value;
        
        toggleLoader(true);
        
        try {
            await new Promise(r => setTimeout(r, 800));

            const response = await fetch(`/api/v1/shuttle/stops/status`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    stop_name: stopName,
                    time_of_day: timeOfDay
                })
            });
            
            if (!response.ok) throw new Error('API Error');
            const data = await response.json();
            
            const congestionLabel = data.congestion_level === 'High' ? '혼잡' : (data.congestion_level === 'Medium' ? '보통' : '여유');
            const barClass = data.congestion_level === 'High' ? 'fill-high' : (data.congestion_level === 'Medium' ? 'fill-medium' : 'fill-low');
            let barWidth = data.congestion_level === 'High' ? '90%' : (data.congestion_level === 'Medium' ? '50%' : '20%');

            const statusBadge = data.can_board 
                ? `<div class="status-badge status-valid"><i data-lucide="check-circle"></i> 탑승 가능</div>`
                : `<div class="status-badge status-invalid"><i data-lucide="alert-circle"></i> 탑승 불가 (만차 진입)</div>`;

            predictionResult.innerHTML = `
                <div class="pred-card">
                    <div class="pred-header">
                        <h3>${data.stop_name} 분석 결과</h3>
                        ${statusBadge}
                    </div>
                    
                    <div class="pred-metrics">
                        <div class="metric-box">
                            <div class="metric-title">예상 대기 인원</div>
                            <div class="metric-value highlight">${data.expected_waiting}명</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-title">진입 버스 여유 공간</div>
                            <div class="metric-value">${data.bus_capacity_left}석</div>
                        </div>
                    </div>

                    <div class="congestion-bar-container">
                        <div class="congestion-label">
                            <span>정류장 혼잡도 예측</span>
                            <span style="font-weight:600">${congestionLabel}</span>
                        </div>
                        <div class="progress-track">
                            <div class="progress-fill ${barClass}" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
            `;
            
            predictionResult.classList.remove('hidden');
            lucide.createIcons();

            // Trigger animation
            setTimeout(() => {
                const fill = predictionResult.querySelector('.progress-fill');
                if(fill) fill.style.width = barWidth;
            }, 50);

        } catch (error) {
            console.error(error);
            predictionResult.innerHTML = `<p class="empty-state" style="color:var(--danger)">예측 서버 모델에 연결할 수 없습니다.</p>`;
            predictionResult.classList.remove('hidden');
        } finally {
            toggleLoader(false);
        }
    });
});
