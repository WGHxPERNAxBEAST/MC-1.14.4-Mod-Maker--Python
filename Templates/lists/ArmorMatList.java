package ***AUTHOR***.***MODNAME***.lists;

import ***AUTHOR***.***MODNAME***.main;
import net.minecraft.inventory.EquipmentSlotType;
import net.minecraft.item.IArmorMaterial;
import net.minecraft.item.Item;
import net.minecraft.item.crafting.Ingredient;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.SoundEvents;

public enum ArmorMatList implements IArmorMaterial {
	//***AMOR_MAT_NAME***_mat("***AMOR_MAT_NAME***", 25, new int[] {2, 5, 6, 2}, 22, ***REPAIR_ITEM***, SoundEvents.ITEM_ARMOR_EQUIP_GENERIC, 1.5F)
	//***NEXT_ARMOR_MAT_HERE***
	;
	
	private static final int[] max_damage_array = new int[]{13, 15, 16, 11};
	private String name;
	private SoundEvent equipSound;
	private int durability, enchantability;
	private int[] damageReductionAmounts;
	private Item repairItem;
	private float toughness;
	
	private ArmorMatList(String name, int durability, int[] damageReductionAmounts, int enchantability, Item repairItem, SoundEvent equipSound, float toughness) {
		this.name = name;
		this.durability = durability;
		this.damageReductionAmounts = damageReductionAmounts;
		this.enchantability = enchantability;
		this.equipSound = equipSound;
		this.repairItem = repairItem;
		this.toughness = toughness;
	}

	@Override
	public int getDamageReductionAmount(EquipmentSlotType slot) {
		return this.damageReductionAmounts[slot.getIndex()];
	}

	@Override
	public int getDurability(EquipmentSlotType slot) {
		return max_damage_array[slot.getIndex()] * this.durability;
	}

	@Override
	public int getEnchantability() {
		return this.enchantability;
	}

	@Override
	public String getName() {
		return main.modid + ":" + this.name;
	}

	@Override
	public Ingredient getRepairMaterial() {
		return Ingredient.fromItems(this.repairItem);
	}

	@Override
	public SoundEvent getSoundEvent() {
		return this.equipSound;
	}

	@Override
	public float getToughness() {
		return this.toughness;
	}
}
