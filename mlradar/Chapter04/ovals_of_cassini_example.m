%% Cassini ovals example
% Created by: Lee A. Harrison
% On: 7/1/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Number of points in the curve
N = 100000;

% Boltzmann's constant
k = 1.38064852e-23;

% Speed of light (ms)
c = 299792458;

% Receiver noise figure (dB)
noise_figure = lin(6);

% System temperature (K)
system_temperature = 290;

% Separation distance (m)
D = 60e3;

% Peak transmit power (W)
peak_power = 100.0e3;

% Tx/Rx antenna gain (dB)
transmit_antenna_gain = lin(30.0);
receive_antenna_gain = lin(30.0);

% Operating frequency (Hz)
frequency = 1.0e9;

% Bistatic target radar cross section (dBsm)
bistatic_target_rcs = lin(10.0);

% Receiver bandwidth (Hz)
bandwidth = 10.0e6;

% Tx/Rx losses (dB)
transmit_losses = lin(4);
receive_losses = lin(3);

% Calculate the wavelength (m)
wavelength = 3e8 / frequency;

% Parameters for Cassini ovals equation
% r^4 + a^4 - 2 a^2 r^2 (1 + cos(2 theta)) = b^4
a = D * 0.5;

bistatic_range_factor = (peak_power * transmit_antenna_gain * receive_antenna_gain * wavelength^2 * bistatic_target_rcs)/...
    ((4.0 * pi)^3 * k * system_temperature * bandwidth * noise_figure * transmit_losses * receive_losses);

% Full angle sweep
t = linspace(0, 2*pi, N);

% Calculate the point at which a = b
SNR_0 = db(16 * bistatic_range_factor / D^4);

% The list of desired SNRs
SNR = SNR_0 - [6, 3, 0, -3];

% Convert to linear units
SNR = lin(SNR);

% Create the plot
figure; hold on;

% Loop over all the desired SNR curves
for i = 1:length(SNR)
    
    % Parameter for the Cassini ovals
    b = (bistatic_range_factor / SNR(i))^0.25;
    
    % Special case when a > b
    if a > b
        
        % Caculat the +/- curves
        R1 = sqrt(a^2 * (cos(2*t) + sqrt(cos(2*t).^2 - 1 + (b/a)^4)));
        R2 = sqrt(a^2 * (cos(2*t) - sqrt(cos(2*t).^2 - 1 + (b/a)^4)));
        
        % Indices for imaginary parts == 0
        ir1 = imag(R1) == 0;
        ir2 = imag(R2) == 0;
        
        % Plot both parts of the curve
        plot(R1(ir1).*cos(t(ir1))/1e3, R1(ir1).*sin(t(ir1))/1e3, 'k.');
        plot(R2(ir2).*cos(t(ir2))/1e3, R2(ir2).*sin(t(ir2))/1e3, 'k.');        
        
    else
        
        % Calculate the range for continuous curves
        R = sqrt(a^2 * cos(2*t) + sqrt(b^4 - a^4 .* sin(2*t).^2));
        plot(real(R.*cos(t))/1e3, real(R.*sin(t))/1e3, '.');
        
    end
    
    % Update the text for the legend
    legend_text{i} = sprintf('SNR = %.1f\n', db(SNR(i)));
    
end

% Add the titles and labels.
title('Ovals of Cassini');
xlabel('Range (km)');
ylabel('Range (km)');

% Add the Tx/Rx locations
text(-a/1e3, 0, 'Tx');
text( a/1e3, 0, 'Rx');

% Turn on the grid
grid on;

% Add the legend
legend(legend_text);

% Use the plot default settings
plot_settings;
