import json
import asyncio
import re


class Files():

    def setup(self):
        """Sets up the Files object with global variables that will be used within multiple extensions"""
        global member_lists
        global role_lists
        global word_lists
        global commands
        # Opening up the json file with the points for each member
        with open('./JSON/members.json', 'r') as f:
            try:
                member_lists = json.load(f)
            except FileNotFoundError:
                print("members.json file does not exist. Create a json file within the JSON directory.")

        # Opening up the json file with the points for the roles to purchase
        with open('./JSON/roles.json', 'r') as r:
            try:
                role_lists = json.load(r)
            except FileNotFoundError:
                print("roles.json file does not exist. Create a json file within the JSON directory.")

        # Opening up the json file with the list of banned words
        with open('./JSON/words.json', 'r') as w:
            try:
                word_lists = json.load(w)
            except FileNotFoundError:
                print("words.json does not exist. Create a json file within the JSON directory.")

        # Opening up the json file with the list of commands
        with open('./JSON/commands.json', 'r') as c:
            try:
                commands = json.load(c)
            except FileNotFoundError:
                print("commands.json does not exist. Create a json file within the JSON directory.")


    async def dump_members(self):
        """This function dumps the member_lists dictionary
        into the members.json file."""
        with open('./JSON/members.json', 'w') as w:
            try:
                json.dump(member_lists, w)
            except FileNotFoundError:
                print("member_list file does not exist")

    async def dump_roles(self):
        """"This function dumps the role_lists dictionary
        into the roles.json file."""
        with open('./JSON/roles.json', 'w') as w:
            try:
                json.dump(role_lists, w)
            except FileNotFoundError:
                print('role_list file does not exist')

    async def dump_words(self):
        """This function dumps the word_lists list
        into the words.json file."""
        with open('./JSON/words.json', 'w') as w:
            try:
                json.dump(word_lists, w)
            except FileNotFoundError:
                print("word_lists file does not exist")

    async def display(self, member_id: str) -> str:
        """Returns the number of points of a member"""
        return str(member_lists[member_id]['points'])

    async def increase_points(self, member: str):
        """Increases the number of points for a member."""
        member_lists[member]['points'] += 5
        await self.dump_members()

    async def change_points(self, member_id: str, amount: int):
        """Sets the number of points for a member."""
        member_lists[member_id]['points'] = amount
        await self.dump_members()

    async def buy_role(self, member_id: str, amount: int):
        """Changes the user's points to the correct amount after a role purchase"""
        member_lists[member_id]['points'] -= amount
        await self.dump_members()

    async def remove_role(self, role: str):
        """Removes a role if the role exists within the role_lists dictionary"""
        if role in role_lists.keys():
            del role_lists[role]

    async def price(self, role_id: str) -> int:
        """Returns the price of a role."""
        await asyncio.sleep(0.0000001)
        return role_lists[role_id]['purchase_price']

    async def join(self, member_id: int):
        """Inserts a new member within the server"""
        member_lists[str(member_id)] = {'id': member_id, 'points': 0, "warning_count": 0, 'offense_count': 0}
        await self.dump_members()

    async def member_exists(self, member_id):
        """Returns if the user exists or not within the member_lists dictionary object"""
        if member_lists.get(str(member_id)):
            return True
        else:
            return False

    async def roles_return(self) -> dict:
        """Returns the dictionary with all of the roles"""
        return role_lists

    async def set_points(self, exists: str, role: str, points: int):
        """Sets a role with entered amount of points"""
        if exists == "yes":
            role_lists[role] = {'purchase_price': points, 'enabled': True}
            await self.dump_roles()
        else:
            role_lists[role]['purchase_price'] = points
            await self.dump_roles()

    async def warn(self, member: int) -> str:
        """Adds a warning count to a user"""
        member_lists[str(member)]['warning_count'] += 1
        # If the warning count is three, reset it and dump the result
        if member_lists[str(member)]['warning_count'] == 3:
            member_lists[str(member)]['warning_count'] = 0
            await self.dump_members()
            return "0"
        # If the warning count is not three, dump the result and return it
        else:
            count = member_lists[str(member)]['warning_count']
            await self.dump_members()
            return str(count)

    async def offensive_warn(self, member: int) -> str:
        """Adds a count to the offensive count. If the offensive count reaches three. The user will be banned."""
        member_lists[str(member)]['offense_count'] += 1
        # If the offensive count is three, reset it and dump the result
        if member_lists[str(member)]['offense_count'] == 3:
            member_lists[str(member)]['offense_count'] = 0
            await self.dump_members()
            return "0"
        # If the offensive count is not three, dump the result and return it
        else:
            count = member_lists[str(member)]['offense_count']
            await self.dump_members()
            return str(count)

    async def add_word(self, word) -> bool:
        """Adds a new banned word to the ban list of words."""
        # If the word does not exist, add it to the ban list
        new_word = word.lower()
        # If the word does not exist within the list, append it
        if new_word not in word_lists:
            word_lists.append(new_word)
            await self.dump_words()
            return True
        # If it does exist, return False
        else:
            return False

    async def remove_word(self, word) -> bool:
        """Removes a word from the blacklist."""
        word = word.lower()
        # If the word exists within the list, remove it
        if word in word_lists:
            word_lists.remove(word)
            await self.dump_words()
            return True
        # If the word does not exist within the list of words, return False
        else:
            return False

    async def check_word(self,  string) -> bool:
        """This function checks every word to see if there is a match within the ban list of words"""
        new = re.sub(r'[\W_]+', '', string)
        new_string = new.lower()
        if any(word in new_string for word in word_lists):
            return False
        else:
            return True

    async def get_word_list(self):
        """Returns all of the blacklisted words"""
        return word_lists

    async def check_commands(self, string: str) -> bool:
        """This function checks the first word of a message to see if it a command."""
        if string in commands:
            return True
        else:
            return False


file = Files()


async def word_check(ctx):
    result = await asyncio.gather(file.check_word(ctx.message.content))
    result = result[0]
    if not result:
        await ctx.message.delete()
    return result








