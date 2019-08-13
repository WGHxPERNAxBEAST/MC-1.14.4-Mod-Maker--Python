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
	
	public static final ItemGroup baItemGroup = new GroupClass("ba_items", ItemList.tut_item);
	public static final ItemGroup baBlockGroup = new GroupClass("ba_blocks", ItemList.tut_block);
	public static final ItemGroup baToolAndCombatGroup = new GroupClass("ba_t_and_c", ItemList.tut_pick);
	
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

				//ItemList.***BLOCKNAME*** = new ItemBlock(BlockList.***BLOCKNAME***, new Item.Properties().group(***BLOCKINVTAB***)).setRegistryName(BlockList.***BLOCKNAME***.getRegistryName())
			);
			logger.info("Items registered.");
		}
		
		@SubscribeEvent
		public static void registerBlocks(final RegistryEvent.Register<Block> event) {
			event.getRegistry().registerAll (
				//BlockList.***BLOCKNAME*** = new Block(Block.Properties.create(***BLOCKMAT***).hardnessAndResistance(***BLOCKHARDNESS***f, ***BLOCKRESISTANCE***f).lightValue(***BLOCKLIGHTVALUE***).sound(SoundType.***BLOCKSOUND***)).setRegistryName(location("***BLOCKNAME***"))
			);
			logger.info("Blocks registered.");
		}
	}
	
	private static ResourceLocation location(String name) {
		return new ResourceLocation(modid, name);
	}
}
