class TrafficBrain:
    def __init__(self):
        
        self.emission_rates = {'car': 2.4, 'truck': 7.8, 'bus': 9.5, 'motorcycle': 1.1}

    def calculate_emissions(self, counts, signal_status):
        if signal_status == "RED":
            
            return sum(counts.get(v, 0) * self.emission_rates.get(v, 0) for v in self.emission_rates)
        return 0.4 

    def calculate_time(self, counts, queue_len):
        
        weighted_count = counts['car'] + (counts['bus'] * 1.8) + (counts['truck'] * 1.5)
        
        
        queue_bonus = 12 if queue_len > 350 else 0
        ped_bonus = 15 if counts['pedestrian'] > 0 else 0
        
        base_time = 10 + (weighted_count * 3) + queue_bonus + ped_bonus
        return min(base_time, 65)