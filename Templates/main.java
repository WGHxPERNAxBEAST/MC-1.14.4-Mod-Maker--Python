package ***AUTHOR***.***MODNAME***;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import ***AUTHOR***.***MODNAME***.items.ItemCustomAxe;
import ***AUTHOR***.***MODNAME***.items.ItemCustomPickaxe;
import ***AUTHOR***.***MODNAME***.lists.ArmorMatList;
import ***AUTHOR***.***MODNAME***.lists.BlockList;
import ***AUTHOR***.***MODNAME***.lists.ItemList;
import ***AUTHOR***.***MODNAME***.lists.ToolMatList;
import net.minecraft.block.Block;
import net.minecraft.block.SoundType;
import net.minecraft.block.material.Material;
import net.minecraft.inventory.EntityEquipmentSlot;
import net.minecraft.item.Item;
import net.minecraft.item.ItemArmor;
import net.minecraft.item.ItemBlock;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemHoe;
import net.minecraft.item.ItemSpade;
import net.minecraft.item.ItemSword;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod("***MODID***")
public class main {
	
	public static main instance;
	public static final String modid = "***MODID***";
	private static final Logger logger = LogManager.getLogger(modid);
	
	public main() {
		
		FMLJavaModLoadingContext.get().getModEventBus().addListener(this::setup);
		FMLJavaModLoadingContext.get().getModEventBus().addListener(this::clientRegistries);
		
		MinecraftForge.EVENT_BUS.register(this);
	}
	
	//pre-init
	private void setup(final FMLCommonSetupEvent event) {
		logger.info("Setup method registered.");
	}
	
	//client
	private void clientRegistries(final FMLClientSetupEvent event) {
		logger.info("clientRegistries method registered.");
	}
	
	@Mod.EventBusSubscriber(bus=Mod.EventBusSubscriber.Bus.MOD)
	public static class RegistryEvents{
		@SubscribeEvent
		public static void registerItems(final RegistryEvent.Register<Item> event) {
			event.getRegistry().registerAll (
				//ItemList.***ITEM_NAME*** = new Item(new Item.Properties().group(***ITEMINVTAB***).setRegistryName(location("***ITEM_NAME***")))				
				//ItemList.***TOOL_MAT_NAME***_axe = new ItemCustomAxe(ToolMatList.***TOOL_MAT_NAME***_mat, ***AXE_DAMAGE***F, ***AXE_SPEED***F, new Item.Properties().group(***TOOLINVTAB***)).setRegistryName(location("bs_axe"))
				//ItemList.***TOOL_MAT_NAME***_hoe = new HoeItem(ToolMatList.***TOOL_MAT_NAME***_mat, ***HOE_SPEED***F, new Item.Properties().group(***TOOLINVTAB***)).setRegistryName(location("***TOOL_MAT_NAME***_hoe"))
				//ItemList.***TOOL_MAT_NAME***_pick = new ItemCustomPickaxe(ToolMatList.***TOOL_MAT_NAME***_mat, ***PICK_DAMAGE***, ***PICK_SPEED***F, new Item.Properties().group(***TOOLINVTAB***)).setRegistryName(location("***TOOL_MAT_NAME***_pick"))
				//ItemList.***TOOL_MAT_NAME***_shovel = new ShovelItem(ToolMatList.***TOOL_MAT_NAME***_mat, ***SHOVEL_DAMAGE***F, ***SHOVEL_SPEED***F, new Item.Properties().group(***TOOLINVTAB***)).setRegistryName(location("***TOOL_MAT_NAME***_shovel"))
				//ItemList.***TOOL_MAT_NAME***_sword = new SwordItem(ToolMatList.***TOOL_MAT_NAME***_mat, ***SWORD_DAMAGE***, ***SWORD_SPEED***F, new Item.Properties().group(***TOOLINVTAB***)).setRegistryName(location("***TOOL_MAT_NAME***_sword"))
				//ItemList.***ARMOR_MAT_NAME***_helmet = new ArmorItem(ArmorMatList.***ARMOR_MAT_NAME***_mat, EquipmentSlotType.HEAD, new Item.Properties().group(***ARMORINVTAB***)).setRegistryName(location("***ARMOR_MAT_NAME***_helmet"))
				//ItemList.***ARMOR_MAT_NAME***_chestplate = new ArmorItem(ArmorMatList.***ARMOR_MAT_NAME***_mat, EquipmentSlotType.CHEST, new Item.Properties().group(***ARMORINVTAB***)).setRegistryName(location("***ARMOR_MAT_NAME***_chestplate"))
				//ItemList.***ARMOR_MAT_NAME***_leggings = new ArmorItem(ArmorMatList.***ARMOR_MAT_NAME***_mat, EquipmentSlotType.LEGS, new Item.Properties().group(***ARMORINVTAB***)).setRegistryName(location("***ARMOR_MAT_NAME***_leggings"))
				//ItemList.***ARMOR_MAT_NAME***_boots = new ArmorItem(ArmorMatList.***ARMOR_MAT_NAME***_mat, EquipmentSlotType.FEET, new Item.Properties().group(***ARMORINVTAB***)).setRegistryName(location("***ARMOR_MAT_NAME***_boots"))
				//ItemList.***BLOCK_NAME*** = new ItemBlock(BlockList.***BLOCK_NAME***, new Item.Properties().group(***BLOCKINVTAB***)).setRegistryName(BlockList.***BLOCK_NAME***.getRegistryName())
				//***NEXT_ITEM_HERE***
				
				);
			logger.info("Items registered.");
		}
		
		@SubscribeEvent
		public static void registerBlocks(final RegistryEvent.Register<Block> event) {
			event.getRegistry().registerAll (
				//BlockList.***BLOCK_NAME*** = new Block(Block.Properties.create(***BLOCK_MAT***).hardnessAndResistance(***BLOCK_HARDNESS***f, ***BLOCK_RESISTANCE***f).lightValue(***BLOCK_LIGHT_VALUE***).sound(SoundType.***BLOCK_SOUND***)).setRegistryName(location("***BLOCK_NAME***"))
				//***NEXT_BLOCK_HERE***
				
			);
			logger.info("Blocks registered.");
		}
	}
	
	private static ResourceLocation location(String name) {
		return new ResourceLocation(modid, name);
	}
}
