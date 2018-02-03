class CreateJackets < ActiveRecord::Migration
  def change
    create_table :jackets do |t|

      t.timestamps null: false
    end
  end
end
