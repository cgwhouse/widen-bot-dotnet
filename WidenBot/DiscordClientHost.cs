using System;
using System.Reflection;
using System.Threading;
using System.Threading.Tasks;
using Discord;
using Discord.Interactions;
using Discord.WebSocket;
using Microsoft.Extensions.Hosting;

namespace WidenBot
{
    internal sealed class DiscordClientHost : IHostedService
    {
        private readonly DiscordSocketClient _discordSocketClient;
        private readonly InteractionService _interactionService;
        private readonly IServiceProvider _serviceProvider;

        public DiscordClientHost(
            DiscordSocketClient discordSocketClient,
            InteractionService interactionService,
            IServiceProvider serviceProvider
        )
        {
            _discordSocketClient = discordSocketClient;
            _interactionService = interactionService;
            _serviceProvider = serviceProvider;
        }

        public async Task StartAsync(CancellationToken cancellationToken)
        {
            _discordSocketClient.InteractionCreated += InteractionCreated;
            _discordSocketClient.Ready += ClientReady;

            // Bot token
            await _discordSocketClient
                .LoginAsync(
                    TokenType.Bot,
                    "MTE3OTg1NDc5NzI2OTExOTAzNg.Gj1dEB.-XkbIzLF6YU2_7GAqa17r66QocS_ddYVXBUiJY"
                )
                .ConfigureAwait(false);

            await _discordSocketClient.StartAsync().ConfigureAwait(false);
        }

        public async Task StopAsync(CancellationToken cancellationToken)
        {
            _discordSocketClient.InteractionCreated -= InteractionCreated;
            _discordSocketClient.Ready -= ClientReady;

            await _discordSocketClient.StopAsync().ConfigureAwait(false);
        }

        private Task InteractionCreated(SocketInteraction interaction)
        {
            var interactionContext = new SocketInteractionContext(
                _discordSocketClient,
                interaction
            );

            return _interactionService.ExecuteCommandAsync(interactionContext, _serviceProvider);
        }

        private async Task ClientReady()
        {
            await _interactionService
                .AddModulesAsync(Assembly.GetExecutingAssembly(), _serviceProvider)
                .ConfigureAwait(false);

            // Server ID
            await _interactionService
                .RegisterCommandsToGuildAsync(1074901936618344459)
                .ConfigureAwait(false);
        }
    }
}