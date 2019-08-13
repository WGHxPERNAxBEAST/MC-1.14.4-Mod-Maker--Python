package ***AUTHOR***.***MODNAME***;

import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;

public class GroupClass extends ItemGroup{
	
	private Item iconItem;
	
	public GroupClass(String label, Item iconItem) {
		super(label);
		this.iconItem = iconItem;
	}

	@Override
	public ItemStack createIcon() {
		return new ItemStack(this.iconItem);
	}
	
}
