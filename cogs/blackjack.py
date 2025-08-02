import discord
from discord.ext import commands
import random

BJ_names = ['bj', 'Bj', 'BJ', 'Blackjack', '21']
cards = {
    2: ['♠️', '♣️', '♥️', '♦️'],
    3: ['♠️', '♣️', '♥️', '♦️'],
    4: ['♠️', '♣️', '♥️', '♦️'],
    5: ['♠️', '♣️', '♥️', '♦️'],
    6: ['♠️', '♣️', '♥️', '♦️'],
    7: ['♠️', '♣️', '♥️', '♦️'],
    8: ['♠️', '♣️', '♥️', '♦️'],
    9: ['♠️', '♣️', '♥️', '♦️'],
    10: ['♠️', '♣️', '♥️', '♦️'],
    11: ['♠️', '♣️', '♥️', '♦️']  # 11 represents Ace
}

def hand_value(hand):
    values = [card[0] for card in hand]
    total = sum(values)
    aces = values.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def display_hand(hand):
    return ' '.join(f"{v}{s}" for v, s in hand)

class BlackJackView(discord.ui.View):
    def __init__(self, player_hand, dealer_hand, ctx):
        super().__init__(timeout=60)
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.ctx = ctx
        self.game_over = False

    async def update_message(self, interaction):
        player_total = hand_value(self.player_hand)
        dealer_display = f"{self.dealer_hand[0][0]}{self.dealer_hand[0][1]} ❓"
        desc = (
            f'🃏 Your hand: {display_hand(self.player_hand)} (Total: {player_total})\n'
            f'🤖 Dealer hand: {dealer_display}'
        )
        await interaction.response.edit_message(content=desc, view=self)

    def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        self.game_over = True

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("This isn't your game!", ephemeral=True)
        if self.game_over:
            return await interaction.response.send_message("The game is already over!", ephemeral=True)

        value = random.choice(list(cards.keys()))
        suit = random.choice(cards[value])
        self.player_hand.append((value, suit))
        total = hand_value(self.player_hand)

        if total > 21:
            # Dealer draws after player busts
            while hand_value(self.dealer_hand) < 17:
                value = random.choice(list(cards.keys()))
                suit = random.choice(cards[value])
                self.dealer_hand.append((value, suit))
            dealer_total = hand_value(self.dealer_hand)
            desc = (
                f"💥 You busted! Your hand: {display_hand(self.player_hand)} (Total: {total})\n"
                f"🤖 Dealer had: {display_hand(self.dealer_hand)} (Total: {dealer_total})"
            )
            self.disable_all_items()
            try:
                await interaction.response.edit_message(content=desc, view=self)
            except discord.InteractionResponded:
                await interaction.edit_original_response(content=desc, view=self)
        else:
            await self.update_message(interaction)

    @discord.ui.button(label='Stand', style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("This isn't your game!", ephemeral=True)
        if self.game_over:
            return await interaction.response.send_message("The game is already over!", ephemeral=True)

        while hand_value(self.dealer_hand) < 17:
            value = random.choice(list(cards.keys()))
            suit = random.choice(cards[value])
            self.dealer_hand.append((value, suit))

        player_total = hand_value(self.player_hand)
        dealer_total = hand_value(self.dealer_hand)

        if dealer_total > 21 or player_total > dealer_total:
            result = '🎉 You win!'
        elif dealer_total > player_total:
            result = '🤖 Dealer wins!'
        else:
            result = "🤝 It's a tie!"

        desc = (
            f"🃏 Your hand: {display_hand(self.player_hand)} (Total: {player_total})\n"
            f"🤖 Dealer's hand: {display_hand(self.dealer_hand)} (Total: {dealer_total})\n\n"
            f"**{result}**"
        )

        self.disable_all_items()

        try:
            await interaction.response.edit_message(content=desc, view=self)
        except discord.InteractionResponded:
            await interaction.edit_original_response(content=desc, view=self)

    async def on_timeout(self):
        # Disable buttons when view times out
        if not self.game_over:
            self.disable_all_items()
            channel = self.ctx.channel
            try:
                message = await channel.fetch_message(self.message_id)
                await message.edit(view=self)
            except Exception:
                pass

class blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="blackjack", aliases=BJ_names)
    async def blackjack(self, ctx):
        """Play a game of blackjack against the bot."""
        def draw_card():
            value = random.choice(list(cards.keys()))
            suit = random.choice(cards[value])
            return (value, suit)

        player_hand = [draw_card(), draw_card()]
        dealer_hand = [draw_card(), draw_card()]

        view = BlackJackView(player_hand, dealer_hand, ctx)
        content = (
            f"🃏 Your hand: {display_hand(player_hand)} (Total: {hand_value(player_hand)})\n"
            f"🤖 Dealer's hand: {dealer_hand[0][0]}{dealer_hand[0][1]} ❓"
        )

        message = await ctx.send(content=content, view=view, delete_after=70)
        await ctx.message.delete()
        view.message_id = message.id  # for timeout editing if needed

async def setup(bot):
    await bot.add_cog(blackjack(bot))
